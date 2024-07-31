import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QLineEdit, QHBoxLayout, QComboBox, QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt
import subprocess

class FirewallApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.check_firewall_status()
    
    def initUI(self):
        self.setWindowTitle('SEF FireWall')
        self.setGeometry(300, 300, 700, 600)
        
        layout = QVBoxLayout()
        
        # Output area
        self.output_label = QLabel('Firewall Output:')
        layout.addWidget(self.output_label)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        
        # Predefined commands dropdown
        self.command_combo = QComboBox(self)
        self.command_combo.addItems(['Show All Rules', 'Flush All Rules', 'Enable Firewall', 'Disable Firewall', 'Check Firewall Status'])
        self.command_combo.currentIndexChanged.connect(self.predefined_command_selected)
        layout.addWidget(self.command_combo)
        
        # Custom command execution area
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText('Enter custom iptables command')
        layout.addWidget(self.command_input)
        
        self.execute_command_button = QPushButton('Execute Command', self)
        self.execute_command_button.clicked.connect(self.execute_custom_command)
        layout.addWidget(self.execute_command_button)
        
        # Buttons for common firewall commands
        common_layout = QHBoxLayout()
        
        self.show_rules_button = QPushButton('Show Rules', self)
        self.show_rules_button.clicked.connect(self.show_rules)
        common_layout.addWidget(self.show_rules_button)
        
        self.flush_rules_button = QPushButton('Flush Rules', self)
        self.flush_rules_button.clicked.connect(self.flush_rules)
        common_layout.addWidget(self.flush_rules_button)
        
        self.enable_firewall_button = QPushButton('Enable Firewall', self)
        self.enable_firewall_button.clicked.connect(self.enable_firewall)
        common_layout.addWidget(self.enable_firewall_button)
        
        self.disable_firewall_button = QPushButton('Disable Firewall', self)
        self.disable_firewall_button.clicked.connect(self.disable_firewall)
        common_layout.addWidget(self.disable_firewall_button)
        
        layout.addLayout(common_layout)
        
        # Form layout for adding rules
        form_layout = QFormLayout()
        
        self.chain_input = QLineEdit(self)
        self.chain_input.setPlaceholderText('INPUT, OUTPUT, FORWARD')
        form_layout.addRow('Chain:', self.chain_input)
        
        self.protocol_input = QLineEdit(self)
        self.protocol_input.setPlaceholderText('tcp, udp, etc.')
        form_layout.addRow('Protocol:', self.protocol_input)
        
        self.source_input = QLineEdit(self)
        self.source_input.setPlaceholderText('Source IP or subnet')
        form_layout.addRow('Source:', self.source_input)
        
        self.destination_input = QLineEdit(self)
        self.destination_input.setPlaceholderText('Destination IP or subnet')
        form_layout.addRow('Destination:', self.destination_input)
        
        self.action_combo = QComboBox(self)
        self.action_combo.addItems(['ACCEPT', 'REJECT', 'DROP'])
        form_layout.addRow('Action:', self.action_combo)
        
        layout.addLayout(form_layout)
        
        self.add_rule_button = QPushButton('Add Rule', self)
        self.add_rule_button.clicked.connect(self.add_rule)
        layout.addWidget(self.add_rule_button)
        
        self.remove_rule_button = QPushButton('Remove Rule', self)
        self.remove_rule_button.clicked.connect(self.remove_rule)
        layout.addWidget(self.remove_rule_button)
        
        # Buttons for additional functionalities
        additional_layout = QHBoxLayout()
        
        self.save_config_button = QPushButton('Save Config', self)
        self.save_config_button.clicked.connect(self.save_config)
        additional_layout.addWidget(self.save_config_button)
        
        self.load_config_button = QPushButton('Load Config', self)
        self.load_config_button.clicked.connect(self.load_config)
        additional_layout.addWidget(self.load_config_button)
        
        self.clear_output_button = QPushButton('Clear Output', self)
        self.clear_output_button.clicked.connect(self.clear_output)
        additional_layout.addWidget(self.clear_output_button)
        
        layout.addLayout(additional_layout)
        
        self.setLayout(layout)
    
    def predefined_command_selected(self):
        command_map = {
            'Show All Rules': 'sudo iptables -L -v -n',
            'Flush All Rules': 'sudo iptables -F',
            'Enable Firewall': 'sudo ufw enable',
            'Disable Firewall': 'sudo ufw disable',
            'Check Firewall Status': 'sudo ufw status'
        }
        command = command_map.get(self.command_combo.currentText(), '')
        if command:
            self.run_command(command)
    
    def execute_custom_command(self):
        command = self.command_input.text()
        self.run_command(command)
    
    def show_rules(self):
        self.run_command('sudo iptables -L -v -n')
    
    def flush_rules(self):
        self.run_command('sudo iptables -F')
    
    def enable_firewall(self):
        self.run_command('sudo ufw enable')
    
    def disable_firewall(self):
        self.run_command('sudo ufw disable')
    
    def add_rule(self):
        chain = self.chain_input.text()
        protocol = self.protocol_input.text()
        source = self.source_input.text()
        destination = self.destination_input.text()
        action = self.action_combo.currentText()
        
        command = f'sudo iptables -A {chain} -p {protocol} -s {source} -d {destination} -j {action}'
        self.run_command(command)
    
    def remove_rule(self):
        chain = self.chain_input.text()
        protocol = self.protocol_input.text()
        source = self.source_input.text()
        destination = self.destination_input.text()
        action = self.action_combo.currentText()
        
        command = f'sudo iptables -D {chain} -p {protocol} -s {source} -d {destination} -j {action}'
        self.run_command(command)
    
    def save_config(self):
        command = 'sudo iptables-save > /etc/iptables/rules.v4'
        self.run_command(command)
    
    def load_config(self):
        command = 'sudo iptables-restore < /etc/iptables/rules.v4'
        self.run_command(command)
    
    def clear_output(self):
        self.output.clear()
    
    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.output.append(f'Command: {command}\nOutput:\n{result.stdout}\nError:\n{result.stderr}')
            if "Status: active" in result.stdout:
                self.output.append("Firewall is active and enabled on system startup")
        except Exception as e:
            self.output.append(f'Failed to run command: {command}\nError: {str(e)}')
            QMessageBox.critical(self, 'Error', f'Failed to run command: {str(e)}')
    
    def check_firewall_status(self):
        command = 'sudo ufw status'
        self.run_command(command)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirewallApp()
    ex.show()
    sys.exit(app.exec_())

