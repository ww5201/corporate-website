package com.zhuoyi.sdk.model;

import com.google.gson.annotations.SerializedName;
import java.util.List;

/**
 * 订单数据模型
 */
public class Order {

    @SerializedName("id")
    private String id;

    @SerializedName("orderNo")
    private String orderNo;

    @SerializedName("productId")
    private String productId;

    @SerializedName("productName")
    private String productName;

    @SerializedName("amount")
    private double amount;

    @SerializedName("status")
    private String status;

    @SerializedName("customerName")
    private String customerName;

    @SerializedName("customerPhone")
    private String customerPhone;

    @SerializedName("remark")
    private String remark;

    @SerializedName("createdAt")
    private long createdAt;

    // Getters & Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getOrderNo() { return orderNo; }
    public void setOrderNo(String orderNo) { this.orderNo = orderNo; }
    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }
    public String getCustomerPhone() { return customerPhone; }
    public void setCustomerPhone(String customerPhone) { this.customerPhone = customerPhone; }
    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }
    public long getCreatedAt() { return createdAt; }
    public void setCreatedAt(long createdAt) { this.createdAt = createdAt; }

    /** 订单状态中文描述 */
    public String getStatusText() {
        switch (status) {
            case "pending": return "待确认";
            case "confirmed": return "已确认";
            case "producing": return "生产中";
            case "shipping": return "配送中";
            case "completed": return "已完成";
            case "cancelled": return "已取消";
            default: return "未知";
        }
    }
}
