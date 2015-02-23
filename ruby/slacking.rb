#!/usr/bin/env ruby

# Slack API Using Ruby Gem

# Preload credentials from file
load '.config/creds'

require 'slack'

class Slacker

  attr_accessor :client, :user, :user_id, :team, :team_id

  def initialize(token=TOKEN)
    @client = Slack.client(
      options = { token: token,
                  user_agent: "Netuoso API for Slack - v1" }
                )
    @user = auth_user['user']
    @user_id = auth_user['user_id']
    @team = auth_user['team']
    @team_id = auth_user['team_id']
  end

  def auth_user
    @client.auth_test
  end

  def get_presence(user=@user_id)
    @client.users_getPresence(options = {user: user})
  end

  def set_presence(presence,user=@user_id)
    # Presence = Active / Away
    @client.presence_set(options = {user: user, presence: presence})
  end

  def users_list(type='all')
    users = []
    if type == 'all'
      @client.users_list['members'].each { |x| users << x }
    elsif type == 'admin'
      @client.users_list['members'].each { |x| x['is_admin'] == true ? users << x : false }
    elsif type == 'bot'
      @client.users_list['members'].each { |x| x['is_bot'] == true ? users << x : false }
    end
    # p "Listing #{users.count} users:\n"
    users
  end


end
