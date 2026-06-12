package com.zhuoyi.sdk.model;

import com.google.gson.annotations.SerializedName;
import java.util.List;

/**
 * 产品数据模型
 */
public class Product {

    @SerializedName("id")
    private String id;

    @SerializedName("name")
    private String name;

    @SerializedName("category")
    private String category;

    @SerializedName("price")
    private double price;

    @SerializedName("originalPrice")
    private double originalPrice;

    @SerializedName("image")
    private String image;

    @SerializedName("description")
    private String description;

    @SerializedName("sales")
    private int sales;

    @SerializedName("status")
    private int status;

    // Getters & Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
    public double getOriginalPrice() { return originalPrice; }
    public void setOriginalPrice(double originalPrice) { this.originalPrice = originalPrice; }
    public String getImage() { return image; }
    public void setImage(String image) { this.image = image; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public int getSales() { return sales; }
    public void setSales(int sales) { this.sales = sales; }
    public int getStatus() { return status; }
    public void setStatus(int status) { status = status; }

    @Override
    public String toString() {
        return "Product{id=" + id + ", name='" + name + "', price=" + price + "}";
    }
}
