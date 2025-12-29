import 'package:laconic/laconic.dart';

/// 迁移示例
/// 文件命名格式：migration_YYYYMMDDHHmm.dart
/// 例如：migration_202512291430.dart
class MigrationExample {
  static const name = 'migration_example';

  Future<void> migrate(Laconic laconic) async {
    var count = await laconic.table('migrations').where('name', name).count();
    if (count > 0) return;

    // TODO: 在这里编写你的迁移 SQL
    await laconic.statement('''
      CREATE TABLE example_table(
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
