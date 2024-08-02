from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import logging
from datetime import datetime

# Activer le logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Dictionnaire pour stocker les points des utilisateurs
user_points = {}

# Variable pour stocker la date du dernier point attribué
last_award_date = None

def start(update, context):
    update.message.reply_text('Salut! Utilise /poll pour gagner des points.')

def poll(update, context):
    global last_award_date
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    # Obtenir la date actuelle
    current_date = datetime.now().date()

    # Vérifier si la date actuelle est différente de la dernière date d'attribution
    if last_award_date != current_date:
        # Mettre à jour la date de la dernière attribution
        last_award_date = current_date

        # Incrémenter les points de l'utilisateur
        if user_id in user_points:
            user_points[user_id] += 1
        else:
            user_points[user_id] = 1

        update.message.reply_text(f'{user_name}, tu as maintenant {user_points[user_id]} point(s).')
    else:
        update.message.reply_text(f'Désolé {user_name}, un point a déjà été attribué aujourd\'hui. Réessaie demain!')

def results(update, context):
    if user_points:
        results_message = "Voici les points des utilisateurs :\n"
        for user_id, points in user_points.items():
            user_name = context.bot.get_chat(user_id).first_name
            results_message += f'{user_name}: {points} point(s)\n'
        update.message.reply_text(results_message)
    else:
        update.message.reply_text('Aucun point n\'a été attribué pour le moment.')

def help_command(update, context):
    help_message = (
        "Voici les commandes disponibles :\n"
        "/start - Démarrer l'interaction avec le bot.\n"
        "/poll - Gagner un point (une fois par jour).\n"
        "/results - Voir les points des différents utilisateurs.\n"
        "/help - Voir la liste des commandes disponibles."
    )
    update.message.reply_text(help_message)

def main():
    # Remplace 'TON_TOKEN_API' par le token de ton bot
    updater = Updater("", use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("poll", poll))
    dp.add_handler(CommandHandler("results", results))
    dp.add_handler(CommandHandler("help", help_command))

    # Démarrer le Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()