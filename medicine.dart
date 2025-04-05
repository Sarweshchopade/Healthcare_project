import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class MedicineAvailabilityScreen extends StatefulWidget {
  @override
  _MedicineAvailabilityScreenState createState() => _MedicineAvailabilityScreenState();
}

class _MedicineAvailabilityScreenState extends State<MedicineAvailabilityScreen> {
  TextEditingController _searchController = TextEditingController();
  List<dynamic> _medicines = [];

  Future<void> searchMedicine(String query) async {
    final response = await http.get(Uri.parse('http://localhost:5000/search_medicine?name=$query'));

    if (response.statusCode == 200) {
      setState(() {
        _medicines = json.decode(response.body)['data'];
      });
    } else {
      print("Error fetching medicine data");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Medicine Availability")),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: "Enter medicine name",
                suffixIcon: IconButton(
                  icon: Icon(Icons.search),
                  onPressed: () => searchMedicine(_searchController.text),
                ),
              ),
            ),
            SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: _medicines.length,
                itemBuilder: (context, index) {
                  var medicine = _medicines[index];
                  return Card(
                    child: ListTile(
                      title: Text(medicine['name']),
                      subtitle: Text("Price: \$${medicine['price']} | Stock: ${medicine['stock']}"),
                      trailing: Text("Pharmacy: ${medicine['pharmacy']}"),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
