from typing import Dict

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount, ConversationReference, Activity


class Bot(ActivityHandler):
    """
    Represents a bot that handles various activities in a conversation.
    Used to send a message to the user when a message is received.
    """

    def __init__(self, conversation_references: Dict[str, ConversationReference]):
        self.conversation_references = conversation_references

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        """
        Handles the conversation update activity.

        Args:
            turn_context (TurnContext): The context object for the current turn of the conversation.
        """
        self._add_conversation_reference(turn_context.activity)
        return await super().on_conversation_update_activity(turn_context)

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        """
        Handles the 'members added' activity event.

        Args:
            members_added (List[ChannelAccount]): The list of members added to the conversation.
            turn_context (TurnContext): The context object for the current turn of the conversation.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Listening...")

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Echo back what the user said with the activity's text.
        """
        self._add_conversation_reference(turn_context.activity)
        return await turn_context.send_activity(f"You sent: {turn_context.activity.text}")

    def _add_conversation_reference(self, activity: Activity):
        """
        Adds the conversation reference of the given activity to the conversation_references dictionary.
        """
        conversation_reference = TurnContext.get_conversation_reference(activity)
        self.conversation_references[conversation_reference.user.id] = conversation_reference
