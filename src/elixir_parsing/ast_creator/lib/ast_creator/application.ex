defmodule AstCreator.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      AstCreator.Repo,
      AstCreator.Worker
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: AstCreator.Supervisor]
    IO.puts("starting supervisor")
    Supervisor.start_link(children, opts)
  end
end
