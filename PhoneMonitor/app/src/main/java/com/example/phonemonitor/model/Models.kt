package com.example.phonemonitor.model

import com.google.gson.annotations.SerializedName

data class AppUsageInfo(
    @SerializedName("packageName")
    val packageName: String,

    @SerializedName("appName")
    val appName: String,

    @SerializedName("lastTimeUsed")
    val lastTimeUsed: Long,

    @SerializedName("usageTime")
    val usageTime: Long
)

data class MonitorData(
    @SerializedName("deviceId")
    val deviceId: String,

    @SerializedName("timestamp")
    val timestamp: Long,

    @SerializedName("runningApps")
    val runningApps: List<AppUsageInfo>,

    @SerializedName("totalAppsCount")
    val totalAppsCount: Int
)

data class ApiResponse(
    @SerializedName("success")
    val success: Boolean,

    @SerializedName("message")
    val message: String? = null,

    @SerializedName("id")
    val id: String? = null
)
