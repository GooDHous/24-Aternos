from configparser import ConfigParser
from javascript import require, On
mineflayer = require('mineflayer')
from tkinter import Tk, Label, Button, ttk, Frame, messagebox, Text, Scrollbar, Entry
import threading, os, sys, json
from sys import platform
import time
from datetime import datetime

class MinecraftBot:
    def __init__(self):
        self.bot_instance = None
        self.stop_threads = False
        self.bot_thread = None
        self.is_running = False
        self.locale = {}  # Словарь для хранения локализованных строк

        self.log_file = "console.log"
        self.init_log_file()

        self.config = ConfigParser()
        try:
            if not os.path.exists('config.ini'):
                self.create_default_config()
            self.config.read('config.ini', encoding='utf-8')
            
            # Загрузка локализации
            self.load_locale()
            
        except Exception as e:
            self.log_to_file(f"Configuration error: {str(e)}")
            messagebox.showerror("Configuration Error", f"Failed to load configuration: {str(e)}")
            sys.exit(1)
            
        self.setup_gui()
        
        self.log_message(self.get_locale_text('bot_ready'))
    
    def get_locale_text(self, key):
        """Получает локализованный текст по ключу"""
        return self.locale.get(key, f"[{key}]")
    
    def load_locale(self):
        """Загружает файл локализации на основе настроек конфига"""
        language = self.config.get('bot', 'language', fallback='en_US')
        locale_path = os.path.join('locales', f'{language}.json')
        
        # Проверяем существование файла локализации
        if not os.path.exists(locale_path):
            self.log_to_file(f"Locale file not found: {locale_path}")
            # Пробуем загрузить английскую локализацию как fallback
            fallback_path = os.path.join('locales', 'en_US.json')
            if os.path.exists(fallback_path):
                locale_path = fallback_path
                self.log_to_file(f"Using fallback locale: {fallback_path}")
            else:
                self.log_to_file("No locale files found! Using empty dictionary.")
                self.locale = {}
                return
        
        # Загружаем локализацию из JSON файла
        try:
            with open(locale_path, 'r', encoding='utf-8') as f:
                self.locale = json.load(f)
            self.log_to_file(f"Successfully loaded locale: {language}")
        except Exception as e:
            self.log_to_file(f"Error loading locale file: {str(e)}")
            self.locale = {}
    
    def init_log_file(self):
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"Minecraft Bot Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n")
        except Exception as e:
            print(f"Failed to create log file: {str(e)}")
    
    def log_to_file(self, message):
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(f"Error writing to log: {str(e)}")
    
    def create_default_config(self):
        self.config['server'] = {
            'host': '127.0.0.1', 
            'port': '25565',
            'chat': 'local' 
        }
        self.config['bot'] = {
            'name': 'GooDHous',
            'language': 'en_US'  # Язык по умолчанию
        }
        self.config['command'] = {
            'position': ';pos', 
            'start': ';start', 
            'stop': ';stop'
        }
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
    
    def setup_gui(self):
        # Используем локализованные строки
        title_text = self.get_locale_text('title')
        status_text = self.get_locale_text('status')
        offline_text = self.get_locale_text('offline')
        info_text = self.get_locale_text('info')
        name_text = self.get_locale_text('name')
        server_text = self.get_locale_text('server')
        chat_mode_text = self.get_locale_text('chat_mode')
        start_text = self.get_locale_text('start')
        stop_text = self.get_locale_text('stop')
        console_text = self.get_locale_text('console')
        clear_text = self.get_locale_text('clear')
        send_message_text = self.get_locale_text('send_message')
        send_text = self.get_locale_text('send')
        footer_text = self.get_locale_text('footer')

        self.root = Tk()
        self.root.title(f"{title_text} - {self.config.get('bot', 'name')}")
        self.root.geometry('550x680')
        self.root.resizable(False, False)
        self.root.configure(bg='#2c2f33')
        
        self.apply_forest_dark_theme()
        
        try:
            if platform == "win32":
                self.root.iconbitmap('bot_icon.ico') if os.path.exists('bot_icon.ico') else None
        except:
            pass
        
        main_frame = Frame(self.root, bg='#23272a', bd=2, relief='raised')
        main_frame.pack(padx=15, pady=15, fill='both', expand=True)
        
        title_label = Label(main_frame, text=title_text, 
                           font=('Arial', 18, 'bold'), fg='#7289da', bg='#23272a')
        title_label.pack(pady=(10, 8))
        
        self.status_frame = Frame(main_frame, bg='#2c2f33', bd=1, relief='sunken')
        self.status_frame.pack(pady=6, padx=15, fill='x')
        
        status_title = Label(self.status_frame, text=status_text, 
                            font=('Arial', 10, 'bold'), fg='#ffffff', bg='#2c2f33')
        status_title.pack(pady=(6, 3))
        
        self.status_label = Label(self.status_frame, text=offline_text, 
                                 font=('Arial', 12, 'bold'), fg='#ff0000', bg='#2c2f33')
        self.status_label.pack(pady=(0, 6))
        
        info_frame = Frame(main_frame, bg='#2c2f33', bd=1, relief='sunken')
        info_frame.pack(pady=6, padx=15, fill='x')

        info_title = Label(info_frame, text=info_text, 
                          font=('Arial', 10, 'bold'), fg='#ffffff', bg='#2c2f33')
        info_title.pack(pady=(6, 3))

        name_frame = Frame(info_frame, bg='#2c2f33')
        name_frame.pack(pady=3, fill='x', padx=8)

        name_label = Label(name_frame, text=name_text, 
                          font=('Arial', 9), fg='#ffffff', bg='#2c2f33', width=12, anchor='w')
        name_label.pack(side='left')

        self.name_value = Label(name_frame, text=self.config.get('bot', 'name'), 
                               font=('Arial', 9, 'bold'), fg='#7289da', bg='#2c2f33', anchor='w')
        self.name_value.pack(side='left', padx=(0, 0), fill='x', expand=True)

        server_frame = Frame(info_frame, bg='#2c2f33')
        server_frame.pack(pady=3, fill='x', padx=8)

        server_label = Label(server_frame, text=server_text, 
                            font=('Arial', 9), fg='#ffffff', bg='#2c2f33', width=12, anchor='w')
        server_label.pack(side='left')

        server_text_value = f"{self.config.get('server', 'host')}:{self.config.get('server', 'port')}"
        server_value = Label(server_frame, text=server_text_value, 
                            font=('Arial', 9, 'bold'), fg='#7289da', bg='#2c2f33', anchor='w')
        server_value.pack(side='left', padx=(0, 0), fill='x', expand=True)

        chat_mode_frame = Frame(info_frame, bg='#2c2f33')
        chat_mode_frame.pack(pady=3, fill='x', padx=8)

        chat_mode_label = Label(chat_mode_frame, text=chat_mode_text, 
                               font=('Arial', 9), fg='#ffffff', bg='#2c2f33', width=12, anchor='w')
        chat_mode_label.pack(side='left')

        chat_mode = self.config.get('server', 'chat', fallback='local')
        self.chat_mode_value = Label(chat_mode_frame, text=chat_mode.upper(), 
                                    font=('Arial', 9, 'bold'), fg='#7289da', bg='#2c2f33', anchor='w')
        self.chat_mode_value.pack(side='left', padx=(0, 0), fill='x', expand=True)

        button_frame = Frame(main_frame, bg='#23272a')
        button_frame.pack(pady=10)
        
        self.start_button = Button(button_frame, text=start_text, 
                                  font=('Arial', 10, 'bold'), bg='#43b581', fg='white',
                                  relief='raised', bd=2, width=10, height=1,
                                  command=self.start_bot)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = Button(button_frame, text=stop_text, 
                                 font=('Arial', 10, 'bold'), bg='#f04747', fg='white',
                                 relief='raised', bd=2, width=10, height=1,
                                 command=self.stop_bot, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        console_frame = Frame(main_frame, bg='#2c2f33', bd=1, relief='sunken')
        console_frame.pack(pady=8, padx=15, fill='both', expand=True)
        
        console_title = Label(console_frame, text=console_text, 
                             font=('Arial', 9, 'bold'), fg='#ffffff', bg='#2c2f33')
        console_title.pack(pady=(4, 0), anchor='w', padx=5)
        
        console_text_frame = Frame(console_frame, bg='#23272a')
        console_text_frame.pack(pady=4, padx=4, fill='both', expand=True)
        
        scrollbar = Scrollbar(console_text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.console = Text(console_text_frame, font=('Consolas', 9), fg='#ffffff', bg='#23272a',
                           yscrollcommand=scrollbar.set, wrap='word', height=12)
        self.console.pack(side='left', fill='both', expand=True)
        self.console.config(state='disabled')
        
        scrollbar.config(command=self.console.yview)
        
        clear_button = Button(console_frame, text=clear_text, font=('Arial', 7), 
                             command=self.clear_console, bg='#555', fg='white')
        clear_button.pack(pady=(0, 4), side='right', padx=4)
        
        chat_frame = Frame(main_frame, bg='#23272a')
        chat_frame.pack(pady=8, padx=15, fill='x')
        
        chat_title = Label(chat_frame, text=send_message_text, 
                          font=('Arial', 9, 'bold'), fg='#ffffff', bg='#23272a')
        chat_title.pack(anchor='w', pady=(0, 4))
        
        chat_input_frame = Frame(chat_frame, bg='#23272a')
        chat_input_frame.pack(fill='x')
        
        self.chat_entry = Entry(chat_input_frame, font=('Arial', 9), bg='#2c2f33', fg='white', 
                               insertbackground='white', width=25)
        self.chat_entry.pack(side='left', fill='x', expand=True, padx=(0, 4))
        self.chat_entry.bind('<Return>', lambda event: self.send_chat_message())
        
        self.send_button = Button(chat_input_frame, text=send_text, font=('Arial', 9), 
                                 command=self.send_chat_message, bg='#7289da', fg='white',
                                 state='disabled')
        self.send_button.pack(side='right')
        
        footer = Label(main_frame, text=footer_text, 
                      font=('Arial', 8), fg='#99aab5', bg='#23272a')
        footer.pack(side='bottom', pady=4)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def apply_forest_dark_theme(self):
        # Код темы без изменений
        forest_dark_theme = """
            ttk::style theme create forest-dark -parent clam -settings {
                ttk::style configure . \
                    -background #23272a \
                    -foreground #ffffff \
                    -troughcolor #2c2f33 \
                    -selectbackground #7289da \
                    -selectforeground #ffffff \
                    -fieldbackground #2c2f33 \
                    -font {TkDefaultFont 9} \
                    -borderwidth 1 \
                    -relief flat

                ttk::style map . \
                    -background [list disabled #23272a active #2c2f33] \
                    -foreground [list disabled #666 active #ffffff]

                ttk::style configure TButton \
                    -anchor center \
                    -width 10 \
                    -padding {5 1} \
                    -background #7289da \
                    -foreground #ffffff \
                    -relief raised \
                    -borderwidth 2

                ttk::style map TButton \
                    -background [list disabled #555 active #5a6fc7 pressed #5a6fc7] \
                    -foreground [list disabled #999 active #ffffff pressed #ffffff] \
                    -relief [list pressed sunken active raised]

                ttk::style configure TEntry \
                    -fieldbackground #2c2f33 \
                    -foreground #ffffff \
                    -insertcolor #ffffff \
                    -selectbackground #7289da \
                    -selectforeground #ffffff \
                    -borderwidth 1 \
                    -relief sunken

                ttk::style configure TFrame \
                    -background #23272a

                ttk::style configure TLabel \
                    -background #23272a \
                    -foreground #ffffff

                ttk::style configure TScrollbar \
                    -background #23272a \
                    -troughcolor #2c2f33 \
                    -borderwidth 0 \
                    -relief flat

                ttk::style map TScrollbar \
                    -background [list active #555 disabled #23272a]

                ttk::style configure TNotebook \
                    -background #23272a \
                    -borderwidth 0

                ttk::style configure TNotebook.Tab \
                    -background #2c2f33 \
                    -foreground #99aab5 \
                    -padding {10 5} \
                    -borderwidth 1

                ttk::style map TNotebook.Tab \
                    -background [list selected #7289da active #555] \
                    -foreground [list selected #ffffff active #ffffff]

                ttk::style configure Treeview \
                    -background #2c2f33 \
                    -foreground #ffffff \
                    -fieldbackground #2c2f33

                ttk::style map Treeview \
                    -background [list selected #7289da] \
                    -foreground [list selected #ffffff]

                ttk::style configure Vertical.TScrollbar \
                    -background #23272a \
                    -troughcolor #2c2f33 \
                    -width 12

                ttk::style configure Horizontal.TScrollbar \
                    -background #23272a \
                    -troughcolor #2c2f33 \
                    -width 12
            }
            ttk::style theme use forest-dark
        """
        self.root.eval(forest_dark_theme)
    
    def clear_console(self):
        self.console.config(state='normal')
        self.console.delete(1.0, 'end')
        self.console.config(state='disabled')
        self.log_to_file(self.get_locale_text('console_cleared'))
    
    def log_message(self, message):
        self.log_to_file(message)
        
        self.console.config(state='normal')
        self.console.insert('end', f"> {message}\n")
        
        self.console.see('end')
            
        self.console.config(state='disabled')
        self.root.update_idletasks()
    
    def handle_local_command(self, message):
        try:
            pos_cmd = self.config.get('command', 'position')
            start_cmd = self.config.get('command', 'start')
            stop_cmd = self.config.get('command', 'stop')
            
            if message.startswith(pos_cmd):
                if self.bot_instance:
                    p = self.bot_instance.entity.position
                    response = self.get_locale_text('position_response').format(f"{p.x:.0f}, {p.y:.0f}, {p.z:.0f}")
                    self.log_message(f"[{self.get_locale_text('command')}] {response}")
                else:
                    self.log_message(f"[{self.get_locale_text('command')}] {self.get_locale_text('bot_not_connected')}")
                return True
                    
            elif message.startswith(start_cmd):
                if self.bot_instance:
                    self.bot_instance.setControlState('forward', True)
                    self.bot_instance.setControlState('jump', True)
                    self.bot_instance.setControlState('sprint', True)
                    self.log_message(f"[{self.get_locale_text('command')}] {self.get_locale_text('bot_started')}")
                else:
                    self.log_message(f"[{self.get_locale_text('command')}] {self.get_locale_text('bot_not_connected')}")
                return True
                    
            elif message.startswith(stop_cmd):
                if self.bot_instance:
                    self.bot_instance.clearControlStates()
                    self.log_message(f"[{self.get_locale_text('command')}] {self.get_locale_text('bot_stopped')}")
                else:
                    self.log_message(f"[{self.get_locale_text('command')}] {self.get_locale_text('bot_not_connected')}")
                return True
                
        except Exception as e:
            self.log_message(f"[{self.get_locale_text('command')}] {self.get_locale_text('command_error')} {str(e)}")
            
        return False
    
    def send_chat_message(self):
        message = self.chat_entry.get().strip()
        if not message:
            return
        
        if self.handle_local_command(message):
            self.chat_entry.delete(0, 'end')
            return
            
        if self.bot_instance and self.is_running:
            try:
                self.bot_instance.chat(message)
                self.log_message(self.get_locale_text('message_sent').format(message))
                self.chat_entry.delete(0, 'end')
            except Exception as e:
                self.log_message(self.get_locale_text('send_error').format(str(e)))
                messagebox.showerror(
                    self.get_locale_text('error'), 
                    self.get_locale_text('send_error_dialog').format(str(e))
                )
        else:
            self.log_message(self.get_locale_text('bot_not_running_error'))
            messagebox.showerror(
                self.get_locale_text('error'), 
                self.get_locale_text('bot_not_running_dialog')
            )
    
    def start_bot(self):
        try:
            self.is_running = True
            self.stop_threads = False
            self.bot_thread = threading.Thread(target=self.bot_process)
            self.bot_thread.daemon = True
            self.bot_thread.start()
            
            self.start_button.config(state='disabled', bg='#555')
            self.stop_button.config(state='normal', bg='#f04747')
            self.send_button.config(state='normal', bg='#7289da')
            self.status_label.config(text=self.get_locale_text('starting'), fg='#ffaa00')
            self.log_message(self.get_locale_text('bot_starting'))
            
        except Exception as e:
            self.log_message(self.get_locale_text('start_error').format(str(e)))
            messagebox.showerror(
                self.get_locale_text('error'), 
                self.get_locale_text('start_error_dialog').format(str(e))
            )
    
    def stop_bot(self):
        try:
            self.stop_threads = True
            self.is_running = False
            
            self.start_button.config(state='normal', bg='#43b581')
            self.stop_button.config(state='disabled', bg='#555')
            self.send_button.config(state='disabled', bg='#555')
            self.status_label.config(text=self.get_locale_text('stopping'), fg='#ffaa00')
            self.log_message(self.get_locale_text('bot_stopping'))
            
            if self.bot_instance:
                try:
                    self.bot_instance.quit()
                    self.log_message(self.get_locale_text('disconnect_request'))
                except Exception as e:
                    self.log_message(self.get_locale_text('disconnect_error').format(str(e)))
            
            if self.bot_thread and self.bot_thread.is_alive():
                self.bot_thread.join(timeout=5.0)
                
                if self.bot_thread.is_alive():
                    self.log_message(self.get_locale_text('thread_timeout_warning'))
            
            self.status_label.config(text=self.get_locale_text('offline'), fg='#ff0000')
            self.log_message(self.get_locale_text('bot_stopped'))
            self.log_message(self.get_locale_text('bot_ready'))
            
        except Exception as e:
            self.log_message(self.get_locale_text('stop_error').format(str(e)))
    
    def bot_process(self):
        try:
            self.log_message(self.get_locale_text('creating_bot_instance'))
            bot = mineflayer.createBot({
                'host': self.config.get('server', 'host'),
                'port': self.config.getint('server', 'port'),
                'username': self.config.get('bot', 'name'),
                'version': False
            })
            
            self.bot_instance = bot
            self.log_message(self.get_locale_text('bot_created'))
            
            @On(bot, "login")
            def login(this):
                self.root.after(0, lambda: self.status_label.config(text=self.get_locale_text('online'), fg='#43b581'))
                self.root.after(0, lambda: self.log_message(self.get_locale_text('bot_logged_in')))

                if self.config.has_option('bot', 'login'):
                    try:
                        login_command = self.config.get('bot', 'login')
                        if login_command:
                            bot.chat(login_command)
                            self.root.after(0, lambda: self.log_message(self.get_locale_text('login_command_sent').format(login_command)))
                    except Exception as e:
                        self.root.after(0, lambda: self.log_message(self.get_locale_text('login_command_error').format(e)))
            
            @On(bot, "error")
            def error(err, *a):
                error_msg = self.get_locale_text('connection_error').format(err)
                self.root.after(0, lambda: self.log_message(error_msg))
                self.root.after(0, lambda: self.status_label.config(text=self.get_locale_text('error'), fg='#ff0000'))
            
            @On(bot, "kicked")
            def kicked(this, reason, *a):
                kick_msg = self.get_locale_text('bot_kicked').format(reason)
                self.root.after(0, lambda: self.log_message(kick_msg))
                self.root.after(0, lambda: self.status_label.config(text=self.get_locale_text('kicked'), fg='#ffaa00'))
            
            @On(bot, "chat")
            def handle(this, username, message, *args):
                if username == bot.username:
                    return
                
                self.root.after(0, lambda: self.log_message(f"{username}: {message}"))
                
                chat_mode = self.config.get('server', 'chat', fallback='local')
                
                if message.startswith(self.config.get('command', 'position')):
                    try:
                        p = bot.entity.position
                        response = self.get_locale_text('position_response').format(f"{p.x:.0f}, {p.y:.0f}, {p.z:.0f}")

                        if chat_mode == 'global':
                            response = '!' + response
                        bot.chat(response)
                        self.root.after(0, lambda: self.log_message(self.get_locale_text('coordinates_sent')))
                    except:
                        self.root.after(0, lambda: self.log_message(self.get_locale_text('coordinates_error')))
                
                elif message.startswith(self.config.get('command', 'start')):
                    try:
                        response = self.get_locale_text('bot_activated')
                        if chat_mode == 'global':
                            response = '!' + response
                        bot.chat(response)
                        bot.setControlState('forward', True)
                        bot.setControlState('jump', True)
                        bot.setControlState('sprint', True)
                        self.root.after(0, lambda: self.log_message(self.get_locale_text('bot_started')))
                    except:
                        self.root.after(0, lambda: self.log_message(self.get_locale_text('start_error')))
                
                elif message.startswith(self.config.get('command', 'stop')):
                    try:
                        response = self.get_locale_text('bot_deactivated')
                        if chat_mode == 'global':
                            response = '!' + response
                        bot.chat(response)
                        bot.clearControlStates()
                        self.root.after(0, lambda: self.log_message(self.get_locale_text('bot_stopped')))
                    except:
                        self.root.after(0, lambda: self.log_message(self.get_locale_text('stop_error')))
            
            @On(bot, "spawn")
            def spawn(this):
                p = bot.entity.position
                self.root.after(0, lambda: self.log_message(self.get_locale_text('bot_spawned').format(f"{p.x:.0f}, {p.y:.0f}, {p.z:.0f}")))
            
            @On(bot, "death")
            def death(this):
                self.root.after(0, lambda: self.log_message(self.get_locale_text('bot_died')))
            
            while not self.stop_threads:
                time.sleep(0.5)
            
            try:
                if self.bot_instance:
                    self.bot_instance.quit()
                    self.root.after(0, lambda: self.log_message(self.get_locale_text('bot_disconnected')))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(self.get_locale_text('disconnect_error').format(str(e))))
                
        except Exception as e:
            error_msg = self.get_locale_text('critical_error').format(str(e))
            self.root.after(0, lambda: self.log_message(error_msg))
            self.root.after(0, lambda: self.status_label.config(text=self.get_locale_text('error'), fg='#ff0000'))
            self.root.after(0, lambda: messagebox.showerror(self.get_locale_text('error'), error_msg))
    
    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno(
                self.get_locale_text('confirmation'), 
                self.get_locale_text('exit_confirmation')
            ):
                self.stop_bot()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = MinecraftBot()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application cannot be started: {str(e)}")