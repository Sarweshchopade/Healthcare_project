import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';

class DoctorLocatorScreen extends StatefulWidget {
  @override
  _DoctorLocatorScreenState createState() => _DoctorLocatorScreenState();
}

class _DoctorLocatorScreenState extends State<DoctorLocatorScreen> {
  GoogleMapController? _mapController;
  LatLng _currentLocation = LatLng(37.7749, -122.4194); // Default: San Francisco
  Set<Marker> _markers = {};

  @override
  void initState() {
    super.initState();
    _getUserLocation();
  }

  Future<void> _getUserLocation() async {
    LocationPermission permission = await Geolocator.requestPermission();
    Position position = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
    setState(() {
      _currentLocation = LatLng(position.latitude, position.longitude);
      _markers.add(Marker(
        markerId: MarkerId("current_location"),
        position: _currentLocation,
        infoWindow: InfoWindow(title: "You are here"),
      ));
    });

    _fetchNearbyHospitals();
  }

  void _fetchNearbyHospitals() {
    List<LatLng> hospitalLocations = [
      LatLng(_currentLocation.latitude + 0.01, _currentLocation.longitude + 0.01),
      LatLng(_currentLocation.latitude - 0.01, _currentLocation.longitude - 0.01),
    ];

    setState(() {
      for (var location in hospitalLocations) {
        _markers.add(Marker(
          markerId: MarkerId(location.toString()),
          position: location,
          icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueBlue),
          infoWindow: InfoWindow(title: "Hospital", snippet: "Nearby medical facility"),
        ));
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Doctor & Facility Locator")),
      body: GoogleMap(
        onMapCreated: (GoogleMapController controller) {
          _mapController = controller;
        },
        initialCameraPosition: CameraPosition(target: _currentLocation, zoom: 14),
        markers: _markers,
        myLocationEnabled: true,
      ),
    );
  }
}
