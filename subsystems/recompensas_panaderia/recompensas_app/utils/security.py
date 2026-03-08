from datetime import datetime, timedelta
from flask import request, flash

# In-memory store for failed attempts
# En producción con múltiples servidores se usaría Redis.
# Para este VPS de un solo proceso, un dict global funciona.
_failed_attempts = {}

def get_remote_address():
    """Obtiene la IP real del usuario. ProxyFix en __init__.py ya la procesa."""
    return request.remote_addr

def check_rate_limit(max_attempts=10, block_minutes=3):
    """
    Verifica si la IP actual está bloqueada.
    Se aumentó a 10 intentos y bajó a 3 minutos para mayor fluidez.
    """
    key = get_remote_address()
    
    # NUNCA bloquear localhost o la IP de loopback (evita bloqueos generales por proxy)
    if key in ['127.0.0.1', '::1']:
        return True, 0

    now = datetime.now()
    
    if key in _failed_attempts:
        attempts, first_fail_time, last_fail_time = _failed_attempts[key]
        
        # Si ya pasó el tiempo de bloqueo, resetear
        if now > last_fail_time + timedelta(minutes=block_minutes):
            del _failed_attempts[key]
            return True, 0
        
        if attempts >= max_attempts:
            remaining = (last_fail_time + timedelta(minutes=block_minutes)) - now
            return False, int(remaining.total_seconds() / 60) + 1
            
        return True, attempts
    return True, 0

def record_auth_fail():
    """Registra un fallo de autenticación para la IP actual."""
    key = get_remote_address()
    now = datetime.now()
    
    if key in _failed_attempts:
        attempts, first_fail_time, _ = _failed_attempts[key]
        _failed_attempts[key] = (attempts + 1, first_fail_time, now)
    else:
        _failed_attempts[key] = (1, now, now)

def clear_auth_history():
    """Limpia el historial de fallos para la IP actual tras un login exitoso."""
    key = get_remote_address()
    if key in _failed_attempts:
        del _failed_attempts[key]
