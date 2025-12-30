# Dependencies Configuration

This file contains the dependency configurations for pubspec.yaml.

## Core Dependencies (Always Required)

Add to `pubspec.yaml`:

```yaml
dependencies:
  signals:
  signals_flutter:
  get_it:
  auto_route:
  logger:
  shared_preferences:
  http:

dev_dependencies:
  auto_route_generator:
  build_runner:
```

## Database Dependencies (Optional)

If database support is enabled, add:

```yaml
dependencies:
  laconic:
  path:
  path_provider:
```

## Desktop Dependencies (Optional)

If desktop support is enabled, add:

```yaml
dependencies:
  tray_manager:
  window_manager:
```

## Full Example

Complete pubspec.yaml dependencies section with all options enabled:

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State Management
  signals:
  signals_flutter:

  # Dependency Injection
  get_it:

  # Routing
  auto_route:

  # Utilities
  logger:
  shared_preferences:
  http:

  # Database (optional)
  laconic:
  path:
  path_provider:

  # Desktop (optional)
  tray_manager:
  window_manager:

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints:
  auto_route_generator:
  build_runner:
```

## Dependency Version

All dependencies are using the latest and compatible version.
