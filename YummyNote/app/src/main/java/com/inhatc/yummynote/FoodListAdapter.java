package com.inhatc.yummynote;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;

public class FoodListAdapter extends ArrayAdapter<FoodItem> {

    public FoodListAdapter(Context context, ArrayList<FoodItem> items) {
        super(context, 0, items);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.item_food, parent, false);
        }

        FoodItem item = getItem(position);
        if (item == null) return convertView;

        TextView txtCategoryIcon = convertView.findViewById(R.id.txtCategoryIcon);
        TextView txtName = convertView.findViewById(R.id.txtName);
        TextView txtCategory = convertView.findViewById(R.id.txtCategory);
        TextView txtAddress = convertView.findViewById(R.id.txtAddress);
        TextView txtRating = convertView.findViewById(R.id.txtRating);
        TextView txtPrice = convertView.findViewById(R.id.txtPrice);

        txtName.setText(item.name);
        txtCategory.setText(item.category);
        txtAddress.setText(item.address.isEmpty() ? "위치 없음" : item.address);
        txtRating.setText(getStars(item.rating));
        txtPrice.setText(item.price > 0 ? item.price + "원" : "가격 미등록");
        txtCategoryIcon.setText(getCategoryEmoji(item.category));

        return convertView;
    }

    private String getStars(int rating) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < rating; i++) sb.append("★");
        for (int i = rating; i < 5; i++) sb.append("☆");
        return sb.toString();
    }

    private String getCategoryEmoji(String category) {
        if (category == null) return "🍽️";
        if (category.contains("한식")) return "🍚";
        if (category.contains("중식")) return "🥟";
        if (category.contains("일식")) return "🍣";
        if (category.contains("카페")) return "☕";
        return "🍽️";
    }
}
