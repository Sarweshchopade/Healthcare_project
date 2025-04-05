import 'package:flutter/material.dart';
import 'package:healthcare_project/Symptom.dart';
import 'package:healthcare_project/doctor.dart';
import 'package:healthcare_project/medicine.dart';
import 'package:healthcare_project/auth.dart';

void main() {
  runApp(HealthCareApp());
}

class HealthCareApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Healthcare Assistant',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: AuthScreen(),
    );
  }
}
