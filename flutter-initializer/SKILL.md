---
name: flutter-initializer
description: "Initialize Flutter project with MVVM architecture including signals state management, get_it dependency injection, AutoRoute routing, and optional database support with laconic. Use when the user requests to: (1) Initialize Flutter MVVM architecture, (2) Set up Flutter project structure, (3) Add MVVM pattern to Flutter project. Trigger keywords: Flutter, MVVM, 架构, 初始化."
---

# Flutter MVVM Architecture Initializer

Initialize a Flutter project with a complete MVVM architecture setup, including state management, dependency injection, routing, and optional database support.

## Architecture Components

This skill sets up:

- **State Management**: signals + signals_flutter
- **ViewModel Pattern**: ViewModels hold signals and manage business logic
- **Dependency Injection**: get_it (registers ViewModels only)
- **Routing**: auto_route with code generation
- **Database (Optional)**: laconic query builder with migration system
- **Utilities**: Logger, SharedPreference, and optional desktop support (Tray, Window)

**Architecture Layers**:
- `page/`: UI pages and ViewModels (MVVM)
- `repository/`: Local database operations
- `service/`: Remote API operations (using official http package)
- `entity/`: Data models
- `database/`: Database initialization and migrations (optional)
- `router/`: Route configuration
- `widget/`: Reusable UI components
- `util/`: Utility classes

## Workflow

### Step 1: Project Detection

Check if the current directory is a Flutter project:
- Verify `pubspec.yaml` exists
- Confirm it's a Flutter project (contains `flutter:` section)

If not a Flutter project, inform the user and exit.

### Step 2: User Preferences

Ask the user two questions using AskUserQuestion:

1. **Database Support**: "是否需要数据库模块？"
   - Options: "需要（使用 laconic）", "不需要"

2. **Desktop Support**: "是否需要桌面端支持？"
   - Options: "需要（添加 tray 和 window 工具）", "不需要"

### Step 3: Directory Structure

Create the following directory structure if it doesn't exist:

```
lib/
├── page/          # UI pages and ViewModels
├── repository/    # Local data operations
├── service/       # Remote API operations
├── entity/        # Data models
├── router/        # Route configuration
├── widget/        # Reusable widgets
├── util/          # Utility classes
└── database/      # Database (if enabled)
    └── migration/ # Migration files
```

### Step 4: Copy Template Files

Copy template files from assets to the project:

**Always copy**:
- `assets/utils/logger_util.dart` → `lib/util/logger_util.dart`
- `assets/utils/shared_preference_util.dart` → `lib/util/shared_preference_util.dart`
- `assets/router/app_router.dart` → `lib/router/app_router.dart`
- `assets/di/di.dart` → `lib/di.dart`
- `assets/page/home/home_page.dart` → `lib/page/home/home_page.dart`
- `assets/page/home/home_view_model.dart` → `lib/page/home/home_view_model.dart`

**If database enabled**:
- `assets/database/database.dart` → `lib/database/database.dart`
- `assets/database/migration_example.dart` → `lib/database/migration/migration_YYYYMMDDHHMM.dart`
  - Replace `YYYYMMDDHHMM` with current timestamp
  - Update class name to match filename (e.g., `Migration202512291430`)

**If desktop enabled**:
- `assets/utils/tray_util.dart` → `lib/util/tray_util.dart`
- `assets/utils/window_util.dart` → `lib/util/window_util.dart`

### Step 5: Configure Dependencies

Update `pubspec.yaml` to add required dependencies:

**Core dependencies (always add)**:
```yaml
dependencies:
  signals: ^5.5.3
  signals_flutter: ^5.5.3
  get_it: ^8.0.3
  auto_route: ^9.2.2
  logger: ^2.5.0
  shared_preferences: ^2.3.4
  http: ^1.2.2

dev_dependencies:
  auto_route_generator: ^9.0.0
  build_runner: ^2.4.14
```

**If database enabled**:
```yaml
dependencies:
  laconic:
    git:
      url: https://github.com/CalsRanna/laconic.git
  path: ^1.9.0
  path_provider: ^2.1.5
```

**If desktop enabled**:
```yaml
dependencies:
  tray_manager: ^0.2.4
  window_manager: ^0.4.4
```

### Step 6: Update Router Configuration

Update `lib/router/app_router.dart` to include the home route:

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

Replace `your_app` with the actual package name from pubspec.yaml.

### Step 7: Update Dependency Injection

Update `lib/di.dart` to register HomeViewModel:

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

### Step 8: Install Dependencies

Run the following commands:

```bash
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

### Step 9: Update main.dart

Provide instructions to update `lib/main.dart` with initialization code:

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

## Post-Initialization

After initialization, inform the user:

1. **Directory structure created** with the following organization:
   - `lib/page/` for UI and ViewModels
   - `lib/repository/` for database operations
   - `lib/service/` for API operations
   - `lib/entity/` for data models
   - `lib/util/` for utilities
   - `lib/router/` for routing
   - `lib/widget/` for shared widgets
   - `lib/database/` for database (if enabled)

2. **Dependencies installed**:
   - signals for state management
   - get_it for dependency injection
   - auto_route for routing
   - logger for logging
   - laconic for database (if enabled)
   - tray_manager and window_manager (if desktop enabled)

3. **Next steps**:
   - Run `flutter run` to test the app
   - Create new pages in `lib/page/`
   - Add routes to `lib/router/app_router.dart`
   - Register ViewModels in `lib/di.dart`
   - Run `flutter pub run build_runner build` after adding routes

## Database Migrations

If database is enabled, explain the migration system:

**Creating a new migration**:

1. Create a file in `lib/database/migration/` with format `migration_YYYYMMDDHHmm.dart`
2. Example: `migration_202512291430.dart`

3. Migration file structure:
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

4. Register the migration in `lib/database/database.dart`:
```dart
await Migration202512291430().migrate(laconic);
```

## Architecture Patterns

**ViewModel Pattern**:
- ViewModels use signals for reactive state
- Access via `GetIt.instance.get<YourViewModel>()`
- Dispose resources in `dispose()` method

**Page Pattern**:
- Use `@RoutePage()` annotation for routing
- Get ViewModel from GetIt in `initState()`
- Use `Watch()` widget to observe signals

**Repository Pattern** (if database enabled):
- Repository manages local database operations via DAO
- Use laconic for query building
- Handle offline-first data synchronization

**Service Pattern**:
- Service handles remote API calls
- Use official `http` package for requests
- Return data to ViewModel for processing

## Resources

This skill includes the following template files in the `assets/` directory:

- `utils/`: Logger, SharedPreference, Tray, Window utility templates
- `database/`: Database initialization and migration templates
- `router/`: AutoRoute configuration template
- `di/`: Dependency injection setup template
- `page/home/`: Example home page and ViewModel

These templates are copied to the project during initialization to provide a complete starting structure.
