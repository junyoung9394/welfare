package com.inhatc.yummynote;

public class FoodItem {
    public int id;
    public String name;
    public String category;
    public String address;
    public int price;
    public int rating;
    public String memo;
    public double lat;
    public double lng;

    public FoodItem(int id, String name, String category, String address, int price, int rating, String memo, double lat, double lng) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.address = address;
        this.price = price;
        this.rating = rating;
        this.memo = memo;
        this.lat = lat;
        this.lng = lng;
    }

    public String getListText() {
        return name + " / " + category + " / 별점 " + rating + " / " + price + "원";
    }
}
