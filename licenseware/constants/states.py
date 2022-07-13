from .base_types import BaseTypes



class States(BaseTypes):
    IDLE = 'idle'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'
    TIMEOUT = 'timeout'
    SKIPPED = 'skipped'
    ACTION_REQUIRED = 'action_required'
    REQUEST_ACCEPTED = 'accepted'
    REQUEST_REJECTED = 'rejected'
    REQUEST_PENDING = 'pending'
    REQUEST_REQUESTED = 'requested'
    REQUEST_CANCELLED = 'cancelled'
    REQUEST_REVOKED = 'revoked'
    


