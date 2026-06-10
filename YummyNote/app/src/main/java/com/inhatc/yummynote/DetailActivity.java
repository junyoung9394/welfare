package com.inhatc.yummynote;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class DetailActivity extends Activity {
    FoodDBHelper dbHelper;
    int foodId;
    EditText edtName, edtCategory, edtAddress, edtPrice, edtRating, edtMemo, edtLat, edtLng;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);

        dbHelper = new FoodDBHelper(this);
        foodId = getIntent().getIntExtra("id", -1);

        edtName = findViewById(R.id.edtName);
        edtCategory = findViewById(R.id.edtCategory);
        edtAddress = findViewById(R.id.edtAddress);
        edtPrice = findViewById(R.id.edtPrice);
        edtRating = findViewById(R.id.edtRating);
        edtMemo = findViewById(R.id.edtMemo);
        edtLat = findViewById(R.id.edtLat);
        edtLng = findViewById(R.id.edtLng);

        Button btnMap = findViewById(R.id.btnMap);
        Button btnUpdate = findViewById(R.id.btnUpdate);
        Button btnDelete = findViewById(R.id.btnDelete);
        Button btnBack = findViewById(R.id.btnBack);

        showFood();

        btnMap.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openMap();
            }
        });

        btnUpdate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                updateFood();
            }
        });

        btnDelete.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                deleteDialog();
            }
        });

        btnBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }

    void showFood() {
        FoodItem item = dbHelper.selectFood(foodId);

        if (item == null) {
            Toast.makeText(this, "데이터가 없습니다.", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        edtName.setText(item.name);
        edtCategory.setText(item.category);
        edtAddress.setText(item.address);
        edtPrice.setText(String.valueOf(item.price));
        edtRating.setText(String.valueOf(item.rating));
        edtMemo.setText(item.memo);
        edtLat.setText(String.valueOf(item.lat));
        edtLng.setText(String.valueOf(item.lng));
    }

    void updateFood() {
        String name = edtName.getText().toString();
        String category = edtCategory.getText().toString();
        String address = edtAddress.getText().toString();
        String memo = edtMemo.getText().toString();

        if (name.length() == 0) {
            Toast.makeText(this, "맛집 이름을 입력하세요.", Toast.LENGTH_SHORT).show();
            return;
        }

        int price = changeInt(edtPrice.getText().toString());
        int rating = changeInt(edtRating.getText().toString());
        double lat = changeDouble(edtLat.getText().toString());
        double lng = changeDouble(edtLng.getText().toString());

        int result = dbHelper.updateFood(foodId, name, category, address, price, rating, memo, lat, lng);

        if (result > 0) {
            Toast.makeText(this, "수정되었습니다.", Toast.LENGTH_SHORT).show();
            showFood();
        } else {
            Toast.makeText(this, "수정 실패", Toast.LENGTH_SHORT).show();
        }
    }

    void deleteDialog() {
        AlertDialog.Builder dlg = new AlertDialog.Builder(this);
        dlg.setTitle("삭제 확인");
        dlg.setMessage("삭제할까요?");
        dlg.setPositiveButton("삭제", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                int result = dbHelper.deleteFood(foodId);

                if (result > 0) {
                    Toast.makeText(DetailActivity.this, "삭제되었습니다.", Toast.LENGTH_SHORT).show();
                    finish();
                } else {
                    Toast.makeText(DetailActivity.this, "삭제 실패", Toast.LENGTH_SHORT).show();
                }
            }
        });
        dlg.setNegativeButton("취소", null);
        dlg.show();
    }

    void openMap() {
        double lat = changeDouble(edtLat.getText().toString());
        double lng = changeDouble(edtLng.getText().toString());

        if (lat == 0 || lng == 0) {
            Toast.makeText(this, "위도와 경도를 입력하세요.", Toast.LENGTH_SHORT).show();
            return;
        }

        Intent intent = new Intent(this, MapActivity.class);
        intent.putExtra("name", edtName.getText().toString());
        intent.putExtra("address", edtAddress.getText().toString());
        intent.putExtra("lat", lat);
        intent.putExtra("lng", lng);
        startActivity(intent);
    }

    int changeInt(String value) {
        try {
            return Integer.parseInt(value);
        } catch (Exception e) {
            return 0;
        }
    }

    double changeDouble(String value) {
        try {
            return Double.parseDouble(value);
        } catch (Exception e) {
            return 0;
        }
    }
}
