package com.inhatc.yummynote;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

public class MapActivity extends Activity implements OnMapReadyCallback {
    GoogleMap googleMap;
    String name;
    String address;
    double lat;
    double lng;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map);

        name = getIntent().getStringExtra("name");
        address = getIntent().getStringExtra("address");
        lat = getIntent().getDoubleExtra("lat", 37.4486);
        lng = getIntent().getDoubleExtra("lng", 126.6577);

        TextView txtMapTitle = findViewById(R.id.txtMapTitle);
        txtMapTitle.setText(name + " 위치");

        MapFragment mapFragment = (MapFragment) getFragmentManager().findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }

    @Override
    public void onMapReady(GoogleMap map) {
        googleMap = map;

        LatLng point = new LatLng(lat, lng);
        MarkerOptions marker = new MarkerOptions();
        marker.position(point);
        marker.title(name);
        marker.snippet(address);

        googleMap.addMarker(marker);
        googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(point, 16));
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        menu.add(0, 1, 0, "일반 지도");
        menu.add(0, 2, 0, "위성 지도");
        menu.add(0, 3, 0, "하이브리드 지도");
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (googleMap == null) {
            return true;
        }

        if (item.getItemId() == 1) {
            googleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
        } else if (item.getItemId() == 2) {
            googleMap.setMapType(GoogleMap.MAP_TYPE_SATELLITE);
        } else if (item.getItemId() == 3) {
            googleMap.setMapType(GoogleMap.MAP_TYPE_HYBRID);
        }

        return true;
    }
}
