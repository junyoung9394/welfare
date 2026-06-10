package com.inhatc.yummynote;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

public class AddFoodActivity extends Activity {
    FoodDBHelper dbHelper;
    EditText edtName, edtAddress, edtPrice, edtMemo, edtLat, edtLng;
    RadioGroup radioCategory, radioRating;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_food);

        dbHelper = new FoodDBHelper(this);
        edtName = findViewById(R.id.edtName);
        edtAddress = findViewById(R.id.edtAddress);
        edtPrice = findViewById(R.id.edtPrice);
        edtMemo = findViewById(R.id.edtMemo);
        edtLat = findViewById(R.id.edtLat);
        edtLng = findViewById(R.id.edtLng);
        radioCategory = findViewById(R.id.radioCategory);
        radioRating = findViewById(R.id.radioRating);

        Button btnLocation = findViewById(R.id.btnLocation);
        Button btnSave = findViewById(R.id.btnSave);
        Button btnCancel = findViewById(R.id.btnCancel);

        btnLocation.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getLocation();
            }
        });

        btnSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveFood();
            }
        });

        btnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }

    void getLocation() {
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
            return;
        }

        LocationManager manager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        Location location = null;

        try {
            location = manager.getLastKnownLocation(LocationManager.GPS_PROVIDER);

            if (location == null) {
                location = manager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
            }
        } catch (Exception e) {
            location = null;
        }

        if (location == null) {
            edtLat.setText("37.4486");
            edtLng.setText("126.6577");
            Toast.makeText(this, "현재 위치를 못 찾아서 기본 위치를 넣었습니다.", Toast.LENGTH_SHORT).show();
        } else {
            edtLat.setText(String.valueOf(location.getLatitude()));
            edtLng.setText(String.valueOf(location.getLongitude()));
            Toast.makeText(this, "위치 저장", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == 1) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                getLocation();
            } else {
                edtLat.setText("37.4486");
                edtLng.setText("126.6577");
                Toast.makeText(this, "위치 권한이 없어 기본 위치를 넣었습니다.", Toast.LENGTH_SHORT).show();
            }
        }
    }

    void saveFood() {
        String name = edtName.getText().toString();
        String address = edtAddress.getText().toString();
        String memo = edtMemo.getText().toString();

        if (name.length() == 0) {
            Toast.makeText(this, "맛집 이름을 입력하세요.", Toast.LENGTH_SHORT).show();
            return;
        }

        int categoryId = radioCategory.getCheckedRadioButtonId();
        int ratingId = radioRating.getCheckedRadioButtonId();
        RadioButton categoryButton = findViewById(categoryId);
        RadioButton ratingButton = findViewById(ratingId);

        String category = categoryButton.getText().toString();
        int price = changeInt(edtPrice.getText().toString());
        int rating = changeInt(ratingButton.getText().toString());
        double lat = changeDouble(edtLat.getText().toString());
        double lng = changeDouble(edtLng.getText().toString());

        long result = dbHelper.insertFood(name, category, address, price, rating, memo, lat, lng);

        if (result > 0) {
            Toast.makeText(this, "저장되었습니다.", Toast.LENGTH_SHORT).show();
            finish();
        } else {
            Toast.makeText(this, "저장 실패", Toast.LENGTH_SHORT).show();
        }
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
