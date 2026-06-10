package com.inhatc.yummynote;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;

public class MainActivity extends Activity {
    FoodDBHelper dbHelper;
    EditText edtSearch;
    ListView listFood;
    ArrayList<FoodItem> foodList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        dbHelper = new FoodDBHelper(this);
        edtSearch = findViewById(R.id.edtSearch);
        listFood = findViewById(R.id.listFood);
        Button btnAdd = findViewById(R.id.btnAdd);
        Button btnSearch = findViewById(R.id.btnSearch);

        btnAdd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, AddFoodActivity.class);
                startActivity(intent);
            }
        });

        btnSearch.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String word = edtSearch.getText().toString();

                if (word.length() == 0) {
                    showFoodList("rating DESC");
                } else {
                    foodList = dbHelper.searchFood(word);
                    setListView();
                    Toast.makeText(MainActivity.this, foodList.size() + "개 검색됨", Toast.LENGTH_SHORT).show();
                }
            }
        });

        listFood.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Intent intent = new Intent(MainActivity.this, DetailActivity.class);
                intent.putExtra("id", foodList.get(position).id);
                startActivity(intent);
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        showFoodList("rating DESC");
    }

    void showFoodList(String order) {
        foodList = dbHelper.selectAll(order);
        setListView();
    }

    void setListView() {
        FoodListAdapter adapter = new FoodListAdapter(this, foodList);
        listFood.setAdapter(adapter);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.menuAll) {
            edtSearch.setText("");
            showFoodList("rating DESC");
            Toast.makeText(this, "전체 보기", Toast.LENGTH_SHORT).show();
        } else if (id == R.id.menuRating) {
            showFoodList("rating DESC");
            Toast.makeText(this, "별점 높은 순", Toast.LENGTH_SHORT).show();
        } else if (id == R.id.menuPrice) {
            showFoodList("price ASC");
            Toast.makeText(this, "가격 낮은 순", Toast.LENGTH_SHORT).show();
        } else if (id == R.id.menuName) {
            showFoodList("name ASC");
            Toast.makeText(this, "이름 순", Toast.LENGTH_SHORT).show();
        }

        return true;
    }
}
