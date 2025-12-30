---
name: initializing-flutter
description: "Initialize Flutter project with MVVM architecture including signals state management, get_it dependency injection, AutoRoute routing, and optional database support with laconic. Use when the user requests to: (1) Initialize Flutter MVVM architecture, (2) Set up Flutter project structure, (3) Add MVVM pattern to Flutter project. Trigger keywords: Flutter, MVVM, 架构, 初始化."
---

# Flutter MVVM Architecture Initializer

Initialize a Flutter project with a complete MVVM architecture setup.

## Architecture Overview

- **State Management**: signals + signals_flutter
- **Dependency Injection**: get_it (registers ViewModels only)
- **Routing**: auto_route with code generation
- **Database (Optional)**: laconic query builder with migration system
- **Utilities**: Logger, SharedPreference, and optional desktop support

**Architecture Layers**:
- `page/`: UI pages and ViewModels (MVVM)
- `repository/`: Local database operations
- `service/`: Remote API operations
- `entity/`: Data models
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

Create the following directory structure:

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

Copy template files from this skill's `template/` directory to the project:

**Always copy**:
- `template/util/logger_util.dart` → `lib/util/logger_util.dart`
- `template/util/shared_preference_util.dart` → `lib/util/shared_preference_util.dart`
- `template/router/app_router.dart` → `lib/router/app_router.dart`
- `template/di/di.dart` → `lib/di.dart`
- `template/page/home/home_page.dart` → `lib/page/home/home_page.dart`
- `template/page/home/home_view_model.dart` → `lib/page/home/home_view_model.dart`

**If database enabled**:
- `template/database/database.dart` → `lib/database/database.dart`
- `template/database/migration_example.dart` → `lib/database/migration/migration_YYYYMMDDHHMM.dart`

**If desktop enabled**:
- `template/util/tray_util.dart` → `lib/util/tray_util.dart`
- `template/util/window_util.dart` → `lib/util/window_util.dart`

### Step 5: Configure Dependencies

Update `pubspec.yaml` with required dependencies.

See [DEPENDENCIES.md](DEPENDENCIES.md) for complete dependency configurations.

### Step 6: Update Code Files

Update router, DI, and main.dart with proper configurations.

See [CODE_TEMPLATES.md](CODE_TEMPLATES.md) for complete code template.

### Step 7: Install Dependencies

```bash
flutter pub get
```

### Step 8: Verify Installation

**IMPORTANT**: Check the output for errors. If there are dependency conflicts, resolve them before continuing.

### Step 9: Generate Routes

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### Step 10: Verify Code Generation

**IMPORTANT**: Verify that route generation succeeded.

Check that `lib/router/app_router.gr.dart` was created. If not:
1. Check for errors in the build_runner output
2. Verify `@RoutePage()` annotation is present in page files
3. Re-run the build_runner command

## Post-Initialization Summary

Inform the user:

1. **Directory structure created**
2. **Dependencies installed**
3. **Next steps**:
   - Run `flutter run` to test the app
   - Create new pages in `lib/page/`
   - Add routes to `lib/router/app_router.dart`
   - Register ViewModels in `lib/di.dart`
   - Run `flutter pub run build_runner build` after adding routes

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
- Repository manages local database operations
- Use laconic for query building

**Service Pattern**:
- Service handles remote API calls
- Use official `http` package for requests

## Resources

Template files in this skill's `template/` directory:
- `util/`: Logger, SharedPreference, Tray, Window
- `database/`: Database initialization and migration template
- `router/`: AutoRoute configuration template
- `di/`: Dependency injection setup template
- `page/home/`: Example home page and ViewModel
