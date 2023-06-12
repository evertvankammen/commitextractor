Deze map is voor experimenten Evert 


Query voor join project, commits en filechanges

```postgresql
select g.name, ci.*, f.* from ghsearchselection g 
    join commitinformation ci on g.id = ci.id_project
    join filechanges f on ci.id_project = f.id_project 
                         where f.id_project = :project_id
    order by commit_date_time;
```
Zoek naar spawn 
```postgresql
select g.name, ci.*, f.* from ghsearchselection g  
    join commitinformation ci on g.id = ci.id_project
    join filechanges f on ci.id_project = f.id_project 
                         where f.id_project = :project_id and extension ='.ex' and f.diff_text like '%spawn%'
    order by commit_date_time;
```

Gebruik van virtualenv
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```
Probeer alles in venv te installeren:

Zorg je in de virtual environment zit:
```
source venv/bin/activate
```

dependencies:
   - peewee
   - psycopg2-binary
   - pydriller

start webapp:
```
PYTHONPATH=~/IdeaProjects/commitextractor/ python main.py
```
linux command:
```
lsof -i :5000
pidof python
kill -9 pid
```
install depencies:
Als je venv gebruikt dat wordt alles daar geinstalleerd, anders globaal
```
pip install Flask
pip install peewee
pip install psycopg2-binary
pip install pydriller
```



```
Elixir embedded expressions #{}
"Embedded expression: #{3 + 0.14}"
Multiline strings:
"
This is
a multiline string
"
sigils. ~s()
iex(5)> ~s(This is also a string)
"This is also a string"

iex(6)> ~s("Do... or do not. There is no try." -Master Yoda)
"\"Do... or do not. There is no try.\" -Master Yoda"
heredocs syntax
iex(9)> """
Heredoc must end on its own line """
"""

iex(1)> 'ABC'
'ABC'
character list

iex(2)> [65, 66, 67]
'ABC'

iex(3)> 'Interpolation: #{3 + 0.14}'
'Interpolation: 3.14'
iex(4)> ~c(Character list sigil)
'Character list sigil'
iex(5)> ~C(Unescaped sigil #{3 + 0.14})
'Unescaped sigil \#{3 + 0.14}'
iex(6)> '''
Heredoc
'''
'Heredoc\n'
Character lists aren’t compatible with binary strings.
```

Elixir uses the BEAM virtual created for Erlang. (from Elixir in Action)

Why Erlang/Elixir?
Highly available systems, that run forever, that always respond to client requests.

How to accomplish this:
 - Fault-tolerance — Minimize, isolate, and recover from the effects of runtime errors.
 - Scalability — Handle a load increase by adding more hardware resources without
     changing or redeploying the code.
 - Distribution — Run your system on multiple machines so that others can take over
       if one machine crashes.

If you address these challenges, your systems can constantly provide service with minimal downtime and failures

Parallelism and concurrency are a key parts of the solution.

BEAM runs in one OS process and creates (by default) for each core a OS thread, each OS thread has a scheduler.
Each BEAM scheduler is in reality an OS thread that manages the execution of BEAM
processes. By default, BEAM uses only as many schedulers as there are logical processors available.
Multiple cores are needed for parallelism.

The schedulers use preemption, based on a timeslot, to ensure that all processes get a chance to run.
BEAM processes are lightweight, a few kb, don't share memory, completely isolated.

As already mentioned, processes share no memory. Thus, sending a message to another
process results in a deep copy of the message contents.

A special case where deep-copying doesn’t take place involves binaries (including
strings) that are larger than 64 bytes. These are maintained on a special shared binary
heap, and sending them doesn’t result in a deep copy. This can be useful when you need
to send information to many processes, and the processes don’t need to decode the string.

You may wonder about the purpose of shared-nothing concurrency. First, it simplifies
the code of each individual process. Because processes don’t share memory, you don’t
need complicated synchronization mechanisms such as locks and mutexes. Another
benefit is overall stability: one process can’t compromise the memory of another. This
in turn promotes the integrity and fault-tolerance of the system. Finally, shared-nothing
concurrency makes it possible to implement an efficient garbage collector.



Found mc primitives:
```
Process.sleep()

spawn/1
spawn(fn ->
    expression_1
        ...
    expression_n
end)

spawn(fn -> IO.puts(run_query.("query 1")) end)
```

A process can send a message to another process, the message is put in the mailbox of the receiving process.
These are asynchronous, the sender doesn't wait for a response.
This mailbox is a queue, the messages are processed in the order they arrive.
Limited to memory.

It will process messages by pattern matching.
A message that has another pattern will never be processed, can become a memory problem

How can you resolve this problem? For each server process, you should introduce a
match-all receive clause that deals with unexpected kinds of messages.

```
send(pid, {:an, :arbitrary, :term})

receive do
  pattern_1 -> do_something
  pattern_2 -> do_something_else
end

receive
  {:message, msg} -> do_something(msg)
  other -> log_unknown_message(other) # match all
end

```

A process may keep itself running by using a recursive loop, when using tail recursion it won't consume additional memory.

```
defp loop do
  receive do
   ...
  end
  loop()
end
```

You may register a pid under an atom by using local registration,
means only in same beam instance

```
Process.register(self(), :some_name)
```

Although multiple processes may run in parallel, a single process is always sequential — it either
runs some code or waits for a message. If many processes send messages to a single process, that single process can significantly affect overall throughput.

Theoretically, a process mailbox has an unlimited size. In practice, the mailbox size
is limited by available memory. Thus, if a process constantly falls behind, meaning
messages arrive faster than the process can handle them, the mailbox will constantly
grow and increasingly consume memory. Ultimately, a single slow process may cause an
entire system to crash by consuming all the available memory.

```
GenServer, part of OTP framework
```

All code that implements a server process needs to do the following:

 - Spawn a separate process
 - Run an infinite loop in the process
 - Maintain the process state
 - React to messages
 - Send a response back to the caller

In the current code, we use the term call for synchronous requests. For asynchronous
requests, we’ll use the term cast. This is the naming convention used in OTP, so it’s good
to adopt it.


Some of the compelling features provided by GenServer include the following:
 - Support for calls and casts
 - Customizable timeouts for call requests
 - Propagation of server-process crashes to client processes waiting for a response
 - Support for distributed systems

Note that there’s no special magic behind GenServer. Its code relies on concurrency
primitives explained in chapter 5 and fault-tolerance features explained in chapter 9.

OTP behaviours, sort of contract, a callback function must implement them

The Erlang standard library includes the following OTP behaviours:
 - gen_server — Generic implementation of a stateful server process 
 - supervisor — Provides error handling and recovery in concurrent systems
 - supervisor — Provides error handling and recovery in concurrent systems
 - application — Generic implementation of components and libraries
 - gen_event — Provides event-handling support 
 - gen_statem — Runs a finite state machine in a stateful server process

Elixir provides its own wrappers for the most frequently used behaviours via the
modules GenServer, Supervisor, and Application.

For various reasons, once you start building production systems, you should avoid using
plain processes started with spawn. Instead, all of your processes should be so-called
OTP-compliant processes. Such processes adhere to OTP conventions, they can be used
in supervision trees (described in chapter 9), and errors in those processes are logged
with more details.


Elixir also includes other modules that can be used to run OTP-compliant
processes.

For example, the Task module (https://hexdocs.pm/elixir/Task.html) is
perfect to run one-off jobs that process some input and then stop. The Agent module
(https://hexdocs.pm/elixir/Agent.html) is a simpler (but less powerful) alternative to
GenServer-based processes and is appropriate if the single purpose of the process is to
manage and expose state.

In addition, there are various other OTP-compliant abstractions available via third-party
libraries. For example, GenStage (https://github.com/elixir-lang/gen_stage) can be used
for back-pressure and load control. The Phoenix.Channel module, which is part of the
Phoenix web framework (http://phoenixframework.org/), is used to facilitate bidirec-
tional communication between a client and a web server over protocols such as WebSocket
or HTTP.

spawn
send
receive
Process.register
Process.link
Process.flag
Process.monitor
GenServer
spawn_link
Supervisor


use GenServer .functions
 - start_link
 - call
 - cast
 - stop
 - reply
 - handle_call
 - handle_cast
 - handle_info
 - init
 - terminate
 - code_change

Supervisor.start_link
spawn_link
use Supervisor .functions
 - start_link
 - start_child
 - restart_child
 - stop_child
 - stop
 - terminate
 - init
 - code_change