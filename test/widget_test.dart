import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:financial_tools/main.dart';

void main() {
  testWidgets('Financial Tools app smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const FinancialToolsApp());

    // Verify that the app title is displayed
    expect(find.text('Financial Tools Calculator'), findsOneWidget);
  });
}
