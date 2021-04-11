# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('../pireal/resources/samples/database.pdb', 'pireal/resources/samples'),
    ('../pireal/resources/samples/queries.pqf', 'pireal/resources/samples'),
    ('icon.ico', '.'),
]

a = Analysis(['Z:\\projects\\pireal\\bin\\pireal'],
             pathex=['Z:\\projects\\pireal'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='pireal',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='Z:\\projects\\pireal\\windows\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pireal')
