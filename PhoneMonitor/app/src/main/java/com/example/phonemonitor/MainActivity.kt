package com.example.phonemonitor

import android.app.AppOpsManager
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.Process
import android.provider.Settings
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.phonemonitor.service.UploadService
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var tvTime: TextView
    private lateinit var tvAppsTitle: TextView
    private lateinit var tvAppsList: TextView
    private lateinit var tvHint: TextView
    private lateinit var tvUploadStatus: TextView
    private lateinit var btnToggleService: Button

    private val handler = Handler(Looper.getMainLooper())
    private var isServiceRunning = false

    private val refreshRunnable = object : Runnable {
        override fun run() {
            updateTime()
            if (hasUsagePermission()) {
                loadRunningApps()
            }
            handler.postDelayed(this, 5000)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvTime = findViewById(R.id.tvTime)
        tvAppsTitle = findViewById(R.id.tvAppsTitle)
        tvAppsList = findViewById(R.id.tvAppsList)
        tvHint = findViewById(R.id.tvHint)
        tvUploadStatus = findViewById(R.id.tvUploadStatus)
        btnToggleService = findViewById(R.id.btnToggleService)

        // 如果没有使用情况权限，跳转设置
        if (!hasUsagePermission()) {
            tvHint.text = "请在设置中开启「使用情况访问权限」\n点击此处跳转"
            tvHint.setOnClickListener {
                val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
                startActivity(intent)
            }
            tvHint.setTextColor(0xFF4CAF50.toInt())
        }

        // 启动/停止按钮
        btnToggleService.setOnClickListener {
            if (isServiceRunning) {
                stopUploadService()
            } else {
                startUploadService()
            }
        }

        updateTime()
    }

    override fun onResume() {
        super.onResume()
        handler.post(refreshRunnable)
        checkServiceStatus()

        // 检查权限状态
        if (hasUsagePermission()) {
            tvHint.text = ""
            tvHint.setOnClickListener(null)
            tvHint.setTextColor(0xFF555555.toInt())
        }
    }

    override fun onPause() {
        super.onPause()
        handler.removeCallbacks(refreshRunnable)
    }

    private fun startUploadService() {
        val serviceIntent = Intent(this, UploadService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(serviceIntent)
        } else {
            startService(serviceIntent)
        }
        isServiceRunning = true
        updateServiceUI()
        Toast.makeText(this, "上传服务已启动", Toast.LENGTH_SHORT).show()
    }

    private fun stopUploadService() {
        val serviceIntent = Intent(this, UploadService::class.java)
        stopService(serviceIntent)
        isServiceRunning = false
        updateServiceUI()
        Toast.makeText(this, "上传服务已停止", Toast.LENGTH_SHORT).show()
    }

    private fun checkServiceStatus() {
        // 简单检查：更新按钮状态
        // 实际应该检查服务是否运行
        updateServiceUI()
    }

    private fun updateServiceUI() {
        if (isServiceRunning) {
            btnToggleService.text = "⏹ 停止上传"
            btnToggleService.backgroundTintList = android.content.res.ColorStateList.valueOf(0xFFF44336.toInt())
            tvUploadStatus.text = "上传服务: 运行中 (每5分钟)"
            tvUploadStatus.setTextColor(0xFF4CAF50.toInt())
        } else {
            btnToggleService.text = "▶ 启动上传"
            btnToggleService.backgroundTintList = android.content.res.ColorStateList.valueOf(0xFF4CAF50.toInt())
            tvUploadStatus.text = "上传服务: 未启动"
            tvUploadStatus.setTextColor(0xFF666666.toInt())
        }
    }

    private fun hasUsagePermission(): Boolean {
        val appOps = getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
        val mode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            appOps.unsafeCheckOpNoThrow(
                AppOpsManager.OPSTR_GET_USAGE_STATS,
                Process.myUid(),
                packageName
            )
        } else {
            @Suppress("DEPRECATION")
            appOps.checkOpNoThrow(
                AppOpsManager.OPSTR_GET_USAGE_STATS,
                Process.myUid(),
                packageName
            )
        }
        return mode == AppOpsManager.MODE_ALLOWED
    }

    private fun loadRunningApps() {
        try {
            val usageStatsManager = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
            val calendar = Calendar.getInstance()
            val endTime = calendar.timeInMillis
            calendar.add(Calendar.MINUTE, -5)
            val startTime = calendar.timeInMillis

            val stats = usageStatsManager.queryUsageStats(
                UsageStatsManager.INTERVAL_DAILY,
                startTime,
                endTime
            )

            if (stats.isNullOrEmpty()) {
                tvAppsTitle.text = "正在运行的应用"
                tvAppsList.text = "暂无数据\n\n请确保已开启使用情况访问权限"
                return
            }

            // 过滤最近5分钟内使用的应用
            val recentApps = stats
                .filter { it.lastTimeUsed > startTime }
                .sortedByDescending { it.lastTimeUsed }

            if (recentApps.isEmpty()) {
                tvAppsTitle.text = "正在运行的应用"
                tvAppsList.text = "暂无最近使用的应用"
                return
            }

            tvAppsTitle.text = "正在运行的应用 (${recentApps.size}个)"

            val sb = StringBuilder()
            val sdf = SimpleDateFormat("HH:mm", Locale.getDefault())

            for ((index, stat) in recentApps.withIndex()) {
                if (index >= 30) break

                val appName = try {
                    val appInfo = packageManager.getApplicationInfo(stat.packageName, 0)
                    packageManager.getApplicationLabel(appInfo).toString()
                } catch (e: Exception) {
                    stat.packageName
                }

                val time = sdf.format(Date(stat.lastTimeUsed))
                sb.appendLine("• $appName")
                sb.appendLine("  最后使用: $time")
            }

            tvAppsList.text = sb.toString().trimEnd()

        } catch (e: Exception) {
            tvAppsList.text = "加载失败: ${e.message}"
        }
    }

    private fun updateTime() {
        val sdf = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
        tvTime.text = sdf.format(Date())
    }
}
