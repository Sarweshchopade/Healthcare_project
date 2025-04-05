import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class AuthScreen extends StatefulWidget {
  const AuthScreen({super.key});

  @override
  _AuthScreenState createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();
  bool isLogin = true;
  bool isLoading = false;

  // ✅ Updated to match the correct IP where your Flask server is running
  final String baseUrl = "http://192.168.102.197:5050";

  Future<void> authenticateUser() async {
    setState(() => isLoading = true);

    final url = Uri.parse(
      isLogin ? '$baseUrl/login' : '$baseUrl/register',
    );

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: json.encode({
          "username": _usernameController.text,
          "password": _passwordController.text,
          if (!isLogin) "name": _nameController.text,
        }),
      );

      final responseData = json.decode(response.body);
      print("Response: ${response.statusCode} - ${response.body}");

      if (response.statusCode == 200 || response.statusCode == 201) {
        if (isLogin) {
          SharedPreferences prefs = await SharedPreferences.getInstance();
          prefs.setString("token", responseData["token"]);
        }

        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(isLogin ? "Login Successful" : "Registration Successful"),
        ));
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(responseData["message"] ?? "Authentication Failed"),
        ));
      }
    } catch (e) {
      print("Error: $e");
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text("Network Error!")));
    }

    setState(() => isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(isLogin ? "Login" : "Register")),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            if (!isLogin)
              TextField(
                controller: _nameController,
                decoration: InputDecoration(labelText: "Full Name"),
              ),
            TextField(
              controller: _usernameController,
              decoration: InputDecoration(labelText: "Username"),
            ),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: InputDecoration(labelText: "Password"),
            ),
            SizedBox(height: 20),
            isLoading
                ? CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: authenticateUser,
                    child: Text(isLogin ? "Login" : "Register"),
                  ),
            TextButton(
              onPressed: () {
                setState(() {
                  isLogin = !isLogin;
                });
              },
              child: Text(isLogin
                  ? "Don't have an account? Register"
                  : "Already have an account? Login"),
            )
          ],
        ),
      ),
    );
  }
}
