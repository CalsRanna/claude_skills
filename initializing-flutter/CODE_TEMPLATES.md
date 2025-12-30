# Code Templates

This file contains code template for Flutter MVVM architecture setup. Copy and adapt these template based on your project needs.

## Router Configuration

Update `lib/router/app_router.dart`:

```dart
import 'package:auto_route/auto_route.dart';
import 'package:your_app/router/app_router.gr.dart';

@AutoRouterConfig()
class AppRouter extends RootStackRouter {
  @override
  List<AutoRoute> get routes => [
        AutoRoute(page: HomeRoute.page, initial: true),
      ];
}

final router = AppRouter();
```

**Note**: Replace `your_app` with your actual package name from pubspec.yaml.

## Dependency Injection

Update `lib/di.dart`:

```dart
import 'package:get_it/get_it.dart';
import 'package:your_app/page/home/home_view_model.dart';

class DI {
  static Future<void> ensureInitialized() async {
    final getIt = GetIt.instance;
    getIt.registerLazySingleton<HomeViewModel>(() => HomeViewModel());
  }
}
```

## Main Entry Point

Update `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:your_app/di.dart';
import 'package:your_app/router/app_router.dart';

// If database enabled, add:
// import 'package:your_app/database/database.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // If database enabled, add:
  // await Database.instance.ensureInitialized();

  await DI.ensureInitialized();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Flutter MVVM App',
      routerConfig: router.config(),
    );
  }
}
```

## Database Migration Template

If database is enabled, create migration files in `lib/database/migration/`:

**Filename format**: `migration_YYYYMMDDHHmm.dart` (e.g., `migration_202512291430.dart`)

```dart
import 'package:laconic/laconic.dart';

class Migration202512291430 {
  static const name = 'migration_202512291430';

  Future<void> migrate(Laconic laconic) async {
    var count = await laconic.table('migrations').where('name', name).count();
    if (count > 0) return;

    await laconic.statement('''
      CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at INTEGER NOT NULL
      )
    ''');

    await laconic.table('migrations').insert([
      {'name': name},
    ]);
  }
}
```

Register the migration in `lib/database/database.dart`:
```dart
await Migration202512291430().migrate(laconic);
```
