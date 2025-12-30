import 'package:get_it/get_it.dart';

class DI {
  static Future<void> ensureInitialized() async {
    final getIt = GetIt.instance;
    // TODO: 在这里注册 ViewModel
    // getIt.registerLazySingleton<HomeViewModel>(() => HomeViewModel());
  }
}
