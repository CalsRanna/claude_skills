import 'package:auto_route/auto_route.dart';

@AutoRouterConfig()
class AppRouter extends RootStackRouter {
  @override
  List<AutoRoute> get routes => [
        // TODO: 在这里添加路由
        // AutoRoute(page: HomeRoute.page, initial: true),
      ];
}

final router = AppRouter();
