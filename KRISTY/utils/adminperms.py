from KRISTY import pbot as app


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = await app.get_chat_member(chat_id, user_id)
    if member.privileges:
      if member.privileges.can_post_messages:
        perms.append("can_post_messages")
      if member.privileges.can_edit_messages:
        perms.append("can_edit_messages")
      if member.privileges.can_delete_messages:
        perms.append("can_delete_messages")
      if member.privileges.can_restrict_members:
        perms.append("can_restrict_members")
      if member.privileges.can_promote_members:
        perms.append("can_promote_members")
      if member.privileges.can_change_info:
        perms.append("can_change_info")
      if member.privileges.can_invite_users:
        perms.append("can_invite_users")
      if member.privileges.can_pin_messages:
        perms.append("can_pin_messages")
      if member.privileges.can_manage_video_chats:
        perms.append("can_manage_video_chats")
      return perms
