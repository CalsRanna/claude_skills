import 'dart:io';

import 'package:laconic/laconic.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';

class Database {
  static final Database instance = Database._internal();

  late Laconic laconic;
  final _migrationCreateSql = '''
CREATE TABLE migrations(
  name TEXT NOT NULL
);
''';
  final _checkMigrationExistSql = '''
SELECT name FROM sqlite_master WHERE type='table' AND name='migrations';
''';

  Database._internal();

  Future<void> ensureInitialized() async {
    var directory = await getApplicationSupportDirectory();
    var path = join(directory.path, 'app.db'); // TODO: 修改为你的数据库名称
    var file = File(path);
    var exists = await file.exists();
    if (!exists) {
      await file.create(recursive: true);
    }
    var config = SqliteConfig(path);
    laconic = Laconic.sqlite(
      config,
      listen: (query) {
        // TODO: 可选：添加 SQL 查询日志
        // LoggerUtil.instance.d(query.rawSql);
      },
    );
    await _migrate();
  }

  Future<void> _migrate() async {
    var tables = await laconic.select(_checkMigrationExistSql);
    if (tables.isEmpty) {
      await laconic.statement(_migrationCreateSql);
    }
    // TODO: 在这里添加迁移调用
    // await MigrationYYYYMMDDHHmm().migrate(laconic);
  }
}
