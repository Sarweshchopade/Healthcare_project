import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SymptomAssessmentScreen extends StatefulWidget {
  @override
  _SymptomAssessmentScreenState createState() =>
      _SymptomAssessmentScreenState();
}

class _SymptomAssessmentScreenState extends State<SymptomAssessmentScreen> {
  TextEditingController _controller = TextEditingController();
  String _result = "";

  Future<void> _checkSymptom() async {
    final response = await http.post(
      Uri.parse("http://10.0.2.2:5000/symptom_check"),
      headers: {"Content-Type": "application/json"},
      body: json.encode({"symptoms": _controller.text.split(",")}),
    );

    if (response.statusCode == 200) {
      setState(() {
        _result = json.decode(response.body).toString();
      });
    } else {
      setState(() {
        _result = "No data found.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Symptom Assessment")),
      body: Padding(
        padding: EdgeInsets.all(10),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                labelText: "Enter Symptoms (comma-separated)",
                suffixIcon: IconButton(
                  icon: Icon(Icons.search),
                  onPressed: _checkSymptom,
                ),
              ),
            ),
            SizedBox(height: 20),
            Text(_result, style: TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}