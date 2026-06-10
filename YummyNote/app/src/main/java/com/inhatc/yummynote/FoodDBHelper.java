package com.inhatc.yummynote;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;

public class FoodDBHelper extends SQLiteOpenHelper {

    public FoodDBHelper(Context context) {
        super(context, "food.db", null, 1);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        String sql = "CREATE TABLE foods (" +
                "_id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "name TEXT, " +
                "category TEXT, " +
                "address TEXT, " +
                "price INTEGER, " +
                "rating INTEGER, " +
                "memo TEXT, " +
                "lat REAL, " +
                "lng REAL)";
        db.execSQL(sql);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS foods");
        onCreate(db);
    }

    public long insertFood(String name, String category, String address, int price, int rating, String memo, double lat, double lng) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put("name", name);
        values.put("category", category);
        values.put("address", address);
        values.put("price", price);
        values.put("rating", rating);
        values.put("memo", memo);
        values.put("lat", lat);
        values.put("lng", lng);
        return db.insert("foods", null, values);
    }

    public int updateFood(int id, String name, String category, String address, int price, int rating, String memo, double lat, double lng) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put("name", name);
        values.put("category", category);
        values.put("address", address);
        values.put("price", price);
        values.put("rating", rating);
        values.put("memo", memo);
        values.put("lat", lat);
        values.put("lng", lng);
        return db.update("foods", values, "_id=?", new String[]{String.valueOf(id)});
    }

    public int deleteFood(int id) {
        SQLiteDatabase db = getWritableDatabase();
        return db.delete("foods", "_id=?", new String[]{String.valueOf(id)});
    }

    public FoodItem selectFood(int id) {
        SQLiteDatabase db = getReadableDatabase();
        Cursor cursor = db.rawQuery("SELECT * FROM foods WHERE _id=" + id, null);

        FoodItem item = null;
        if (cursor.moveToNext()) {
            item = makeItem(cursor);
        }

        cursor.close();
        return item;
    }

    public ArrayList<FoodItem> selectAll(String order) {
        SQLiteDatabase db = getReadableDatabase();
        ArrayList<FoodItem> list = new ArrayList<>();
        Cursor cursor = db.rawQuery("SELECT * FROM foods ORDER BY " + order, null);

        while (cursor.moveToNext()) {
            list.add(makeItem(cursor));
        }

        cursor.close();
        return list;
    }

    public ArrayList<FoodItem> searchFood(String word) {
        SQLiteDatabase db = getReadableDatabase();
        ArrayList<FoodItem> list = new ArrayList<>();
        String sql = "SELECT * FROM foods WHERE name LIKE ? OR category LIKE ? OR address LIKE ? OR memo LIKE ? ORDER BY rating DESC";
        String value = "%" + word + "%";
        Cursor cursor = db.rawQuery(sql, new String[]{value, value, value, value});

        while (cursor.moveToNext()) {
            list.add(makeItem(cursor));
        }

        cursor.close();
        return list;
    }

    private FoodItem makeItem(Cursor cursor) {
        int id = cursor.getInt(0);
        String name = cursor.getString(1);
        String category = cursor.getString(2);
        String address = cursor.getString(3);
        int price = cursor.getInt(4);
        int rating = cursor.getInt(5);
        String memo = cursor.getString(6);
        double lat = cursor.getDouble(7);
        double lng = cursor.getDouble(8);

        return new FoodItem(id, name, category, address, price, rating, memo, lat, lng);
    }
}
