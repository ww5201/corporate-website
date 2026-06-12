package com.example.phonemonitor.api

import com.example.phonemonitor.model.ApiResponse
import com.example.phonemonitor.model.MonitorData
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.GET

interface ApiService {
    @POST("api/monitor")
    suspend fun uploadData(@Body data: MonitorData): Response<ApiResponse>

    @GET("api/monitor")
    suspend fun getData(): Response<List<MonitorData>>
}
