# messaging.py
# All user-facing messaging is routed through this interface

def queue_room_description(room):
    """
    Placeholder for describing the player's current room.

    @ignore: stub — no message rendering logic
    """
    pass

def queue_sighting(actor):
    """
    Placeholder for notifying player of a seen actor.

    @ignore: stub — no actor perception feedback
    """
    pass

def queue_player_action_feedback(action):
    """
    Placeholder for showing action results to player.

    @ignore: stub — no action feedback system
    """
    pass

def queue_enemy_action_feedback(actor, action):
    """
    Placeholder for enemy action messaging.

    @ignore: stub — enemy messaging deferred
    """
    pass

def queue_status_message(text):
    """
    Placeholder for simple status message queueing.

    @ignore: stub — UI feedback not implemented
    """
    pass

def flush_message_queue():
    """
    Placeholder for flushing and displaying queued messages.

    @ignore: stub — no message queue system present
    """
    pass
