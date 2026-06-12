package com.example.phonemonitor.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.example.phonemonitor.service.UploadService

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            val serviceIntent = Intent(context, UploadService::class.java)
            context.startForegroundService(serviceIntent)
        }
    }
}
