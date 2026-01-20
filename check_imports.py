import importlib, traceback

modules = [
    'app.routes.camera_routes',
    'app.routes.verification_routes',
    'app.services.camera_service',
    'app.services.pdf_service',
    'app.services.face_verification_service',
    'app.services.face_verification_service_fallback'
]

ok = True
for m in modules:
    try:
        importlib.import_module(m)
    except Exception:
        print('IMPORT_CHECK: FAIL')
        traceback.print_exc()
        ok = False
        break

if ok:
    print('IMPORT_CHECK: OK')
