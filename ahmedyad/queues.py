import os

QUEUE = {}


def add_to_queue(chat_id, ref):
    if chat_id in QUEUE:
        chat_queue = QUEUE[chat_id]
        chat_queue.append([ref])
        return int(len(chat_queue) - 1)
    else:
        QUEUE[chat_id] = [[ref]]
        return 0


def add_list_to_queue(chat_id, pos, additional_list):
    if chat_id in QUEUE:
        chat_queue = QUEUE[chat_id]
        if 0 <= pos < len(chat_queue):
            chat_queue[pos].extend(additional_list)
        else:
            print(f"Invalid position: {pos}.")
    else:
        print(f"No queue found for chat_id: {chat_id}.")


def get_queue(chat_id):
    if chat_id in QUEUE:
        chat_queue = QUEUE[chat_id]
        return chat_queue
    else:
        return []


def pop_an_item(chat_id, delete_file=True):
    if chat_id in QUEUE:
        chat_queue = QUEUE[chat_id]
        if len(chat_queue) > 0:
            if delete_file:
                try:
                    file_path = chat_queue[0][0]
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f'Deleted file: {file_path}')
                except Exception as e:
                    print(f'Error deleting file: {e}')

            chat_queue.pop(0)
            return 1
    return 0


def clear_queue(chat_id, delete_files=True):
    if chat_id in QUEUE:
        try:
            if delete_files:
                chat_queue = QUEUE[chat_id]
                for item in chat_queue:
                    try:
                        file_path = item[0]
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f'Deleted file: {file_path}')
                    except Exception as e:
                        print(f'Error deleting file: {e}')

            QUEUE.pop(chat_id)
        except:
            pass
        return 1
    else:
        return 0