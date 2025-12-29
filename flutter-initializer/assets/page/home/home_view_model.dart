import 'package:signals/signals.dart';

class HomeViewModel {
  final counter = signal(0);

  void increment() {
    counter.value++;
  }

  void decrement() {
    counter.value--;
  }

  void dispose() {
    // 清理资源
  }
}
