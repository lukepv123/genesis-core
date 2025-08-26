### **Como Estender o Genesis Core (Plugins)**

O Genesis Core foi projetado para ser extensível através de um sistema de plugins simples e eficiente. Para adicionar novas funcionalidades, como agentes ou comandos, basta seguir os passos abaixo. O sistema de registro automático cuida do resto para você.

-----

### **1. Criando um Novo Agente**

Agentes são responsáveis por interagir com o usuário e, geralmente, com a LLM. Eles são ativados quando não há comandos locais que se encaixem na requisição do usuário.

**Passo 1: Crie o arquivo do Agente**
Crie um novo arquivo dentro da pasta `src/genesis/plugins/agents/`.

```
src/genesis/plugins/agents/meu_agente.py
```

**Passo 2: Implemente a classe do Agente**
Sua classe deve herdar de `BaseAgent` e ser decorada com `@register_agent`. O decorator se encarrega de registrar seu agente no sistema.

```python
from ...core.base_agent import BaseAgent
from ...core.registry import register_agent

@register_agent
class MeuAgente(BaseAgent):
    name = "meu_agente"
    
    def handle(self, text, context):
        llm = self.services["llm"]
        prompt = self.services["prompts"].get("default", "")
        return llm.complete(prompt, text)
```

**Passo 3 (Opcional): Adicione Configurações**
Se o seu agente precisar de configurações específicas (como um modelo de LLM ou um `system_prompt` diferente), adicione-as no arquivo `config/app.yaml`.

```yaml
agents:
  default_chatbot:
    system_prompt_ref: "default"
  assistant_agent:
    system_prompt_ref: "assistant"
  new_custom_agent:
    system_prompt_ref: "new_custom_prompt"
```
e caso queira criar um prompt diferente tambem, apenas adicione o prompt no arquivo prompts.yaml. Nesse caso, "new_custom_prompt"

```yaml
prompts:
  default: You are Genesis Core's default chatbot. Be concise and helpful.
  assistant: You are a precise technical assistant. When in doubt, ask concise questions.
  new_custom_prompt: aqui voce coloca o que quiser sobre esse agente
```

-----

### **2. Criando um Novo Comando Local**

Comandos locais são ações que o sistema executa sem precisar de uma LLM. Eles têm prioridade sobre os agentes e são ideais para tarefas como verificar a hora, controlar o volume, ou mudar o agente ativo.

**Passo 1: Crie o arquivo do Comando**
Crie um novo arquivo na pasta `src/genesis/plugins/commands/`.

```
src/genesis/plugins/commands/meu_comando.py
```

**Passo 2: Implemente a classe do Comando**
Sua classe deve herdar de `BaseCommand` e ser decorada com `@register_command`. O sistema de registro fará a descoberta automática.

```python
from ...core.base_command import BaseCommand
from ...core.registry import register_command

@register_command
class HoraCommand(BaseCommand):
    name = "hora"
    aliases = ("que horas são", "me diga a hora") # Gatilhos alternativos
    
    def execute(self, text: str) -> str:
        from datetime import datetime
        return f"Agora são: {datetime.now():%H:%M}."
```