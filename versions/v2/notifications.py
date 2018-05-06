from flask import Blueprint, jsonify
from versions.v2.models import db, Notification, User
from versions import login_required

mod = Blueprint('notification_v2', __name__)


@mod.route('/notifications', methods=['GET'])
@login_required
def get_notifications(current_user):
    """Fetch all unread notifications of current user"""
    unread = db.session.query(Notification).join(User).filter(
        User.id==current_user,
        Notification.read_at==None
    ).all()

    if unread:
        for notification in unread:
            notification.read_at = db.func.current_timestamp()
            notification.save()

        return jsonify({'notifications': [
                {
                    'id': notification.id,
                    'recipient_id': notification.recipient.username,
                    'actor': notification.actor,
                    'business_id': notification.business_id,
                    'review_id': notification.review_id,
                    'action': notification.action,
                    'created_at': notification.created_at,
                    'read_at': notification.read_at,
                    'act': notification.actor + notification.action,
                    'url': '/business/{}#review-{}'.format(notification.business_id, notification.review_id)
                } for notification in unread
            ]}), 200

    return jsonify({'warning': 'user has no notifications'}), 404
