from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from datetime import datetime
import os

# Activer le logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Dictionnaire pour stocker les points des utilisateurs
user_points = {}

# Variables pour stocker la date du dernier point attribué et l'utilisateur
last_award_date = None
last_poll_user = None
last_subpoll_user = None  # Nouvel ajout

# Dictionnaire pour stocker la date du dernier point attribué par subpoll pour chaque utilisateur
user_subpoll_date = {}

def start(update, context):
    update.message.reply_text('Salut! Utilise /poll pour gagner des points.')

def poll(update, context):
    global last_award_date, last_poll_user
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    # Obtenir la date actuelle
    current_date = datetime.now().date()

    # Vérifier si la date actuelle est différente de la dernière date d'attribution
    if last_award_date != current_date:
        # Mettre à jour la date de la dernière attribution et l'utilisateur
        last_award_date = current_date
        last_poll_user = user_id
        global last_subpoll_user
        last_subpoll_user = None  # Réinitialiser le dernier utilisateur de subpoll chaque jour

        # Incrémenter les points de l'utilisateur de 3 points
        if user_id in user_points:
            user_points[user_id] += 3
        else:
            user_points[user_id] = 3

        update.message.reply_text(f'{user_name}, tu as maintenant {user_points[user_id]} point(s).')
    else:
        update.message.reply_text(f'Désolé {user_name}, un point a déjà été attribué aujourd\'hui. Réessaie demain!')

def subpoll(update, context):
    global last_award_date, last_poll_user, last_subpoll_user, user_subpoll_date
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    # Obtenir la date actuelle
    current_date = datetime.now().date()

    if last_award_date != current_date:
        update.message.reply_text('Aucun point n\'a été attribué aujourd\'hui. Utilise d\'abord /poll.')
        return

    if user_id == last_poll_user:
        update.message.reply_text(f'Désolé {user_name}, tu ne peux pas attribuer des points car tu as déjà gagné des points aujourd\'hui.')
        return

    if last_subpoll_user == user_id:
        update.message.reply_text(f'Désolé {user_name}, tu ne peux pas gagner un autre point avant demain.')
        return

    if last_subpoll_user is not None:
        update.message.reply_text(f'Désolé {user_name}, un autre utilisateur a déjà gagné un point avec subpoll aujourd\'hui.')
        return

    # Mettre à jour la date de la dernière attribution de points par subpoll
    user_subpoll_date[user_id] = current_date
    last_subpoll_user = user_id  # Mettre à jour l'utilisateur ayant utilisé subpoll aujourd'hui

    # Incrémenter les points de l'utilisateur de 1 point
    if user_id in user_points:
        user_points[user_id] += 1
    else:
        user_points[user_id] = 1

    update.message.reply_text(f'{user_name} gagne 1 point, tu as maintenant {user_points[user_id]} point(s).')

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
        "/poll - Gagner 3 points (une fois par jour).\n"
        "/subpoll <user_id> - Donner 1 point à un autre utilisateur (ne peut pas être celui qui a gagné des points avec /poll).\n"
        "/results - Voir les points des différents utilisateurs.\n"
        "/help - Voir la liste des commandes disponibles."
    )
    update.message.reply_text(help_message)

def main():
    # Remplace 'TON_TOKEN_API' par le token de ton bot
    updater = Updater(os.environ.get("tel_token"), use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("poll", poll))
    dp.add_handler(CommandHandler("subpoll", subpoll))
    dp.add_handler(CommandHandler("results", results))
    dp.add_handler(CommandHandler("help", help_command))

    # Démarrer le Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
