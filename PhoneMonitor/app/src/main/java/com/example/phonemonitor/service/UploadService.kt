package com.example.phonemonitor.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.provider.Settings
import android.app.usage.UsageStatsManager
import android.os.Process
import androidx.core.app.NotificationCompat
import com.example.phonemonitor.R
import com.example.phonemonitor.api.RetrofitClient
import com.example.phonemonitor.model.AppUsageInfo
import com.example.phonemonitor.model.MonitorData
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class UploadService : Service() {

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var uploadJob: kotlinx.coroutines.Job? = null

    companion object {
        private const val CHANNEL_ID = "upload_service"
        private const val NOTIFICATION_ID = 1
        private const val UPLOAD_INTERVAL = 5 * 60 * 1000L // 5分钟
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        startForeground(NOTIFICATION_ID, createNotification("准备上传数据..."))
        startUploading()
        return START_STICKY
    }

    override fun onDestroy() {
        super.onDestroy()
        uploadJob?.cancel()
        serviceScope.cancel()
    }

    private fun startUploading() {
        uploadJob = serviceScope.launch {
            while (true) {
                try {
                    uploadData()
                } catch (e: Exception) {
                    updateNotification("上传失败: ${e.message}")
                }
                delay(UPLOAD_INTERVAL)
            }
        }
    }

    private suspend fun uploadData() {
        updateNotification("正在收集数据...")

        val apps = getRunningApps()
        if (apps.isEmpty()) {
            updateNotification("暂无运行应用数据")
            return
        }

        val data = MonitorData(
            deviceId = createDeviceId(),
            timestamp = System.currentTimeMillis(),
            runningApps = apps,
            totalAppsCount = apps.size
        )

        updateNotification("正在上传 ${apps.size} 个应用数据...")

        try {
            val response = RetrofitClient.apiService.uploadData(data)
            if (response.isSuccessful) {
                val sdf = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
                updateNotification("上传成功 ✓ ${sdf.format(Date())}")
            } else {
                updateNotification("上传失败: ${response.code()}")
            }
        } catch (e: Exception) {
            updateNotification("网络错误: ${e.message?.take(50)}")
        }
    }

    private fun getRunningApps(): List<AppUsageInfo> {
        if (!hasUsagePermission()) return emptyList()

        return try {
            val usageStatsManager = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
            val calendar = Calendar.getInstance()
            val endTime = calendar.timeInMillis
            calendar.add(Calendar.HOUR, -1)  // 最近1小时
            val startTime = calendar.timeInMillis

            val stats = usageStatsManager.queryUsageStats(
                UsageStatsManager.INTERVAL_DAILY,
                startTime,
                endTime
            ) ?: return emptyList()

            stats
                .filter { it.lastTimeUsed > startTime }
                .sortedByDescending { it.lastTimeUsed }
                .take(50)
                .map { stat ->
                    val appName = try {
                        val appInfo = packageManager.getApplicationInfo(stat.packageName, 0)
                        packageManager.getApplicationLabel(appInfo).toString()
                    } catch (e: Exception) {
                        stat.packageName
                    }
                    AppUsageInfo(
                        packageName = stat.packageName,
                        appName = appName,
                        lastTimeUsed = stat.lastTimeUsed,
                        usageTime = stat.totalTimeInForeground
                    )
                }
        } catch (e: Exception) {
            emptyList()
        }
    }

    private fun hasUsagePermission(): Boolean {
        val appOps = getSystemService(Context.APP_OPS_SERVICE) as android.app.AppOpsManager
        val mode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            appOps.unsafeCheckOpNoThrow(
                android.app.AppOpsManager.OPSTR_GET_USAGE_STATS,
                Process.myUid(),
                packageName
            )
        } else {
            @Suppress("DEPRECATION")
            appOps.checkOpNoThrow(
                android.app.AppOpsManager.OPSTR_GET_USAGE_STATS,
                Process.myUid(),
                packageName
            )
        }
        return mode == android.app.AppOpsManager.MODE_ALLOWED
    }

    private fun createDeviceId(): String {
        return "${Build.MODEL}_${android.provider.Settings.Secure.getString(
            contentResolver,
            Settings.Secure.ANDROID_ID
        )?.take(8)}"
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "数据上传服务",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "后台上传监控数据"
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(text: String): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("早点休息")
            .setContentText(text)
            .setSmallIcon(R.drawable.ic_monitor)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    private fun updateNotification(text: String) {
        val manager = getSystemService(NotificationManager::class.java)
        manager.notify(NOTIFICATION_ID, createNotification(text))
    }
}
