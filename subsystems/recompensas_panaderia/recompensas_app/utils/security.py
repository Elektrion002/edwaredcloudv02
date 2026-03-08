from datetime import datetime, timedelta
from flask import request, flash

# In-memory store for failed attempts
# En producción con múltiples servidores se usaría Redis.
# Para este VPS de un solo proceso, un dict global funciona.
_failed_attempts = {}

def get_remote_address():
    """Obtiene la IP real del usuario, manejando el proxy de Nginx."""
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

def check_rate_limit(max_attempts=5, block_minutes=5):
    """
    Verifica si la IP actual está bloqueada.
    Retorna (is_allowed, remaining_minutes)
    """
    key = get_remote_address()
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
