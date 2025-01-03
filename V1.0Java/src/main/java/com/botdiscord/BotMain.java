package com.botdiscord;

import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;

public class BotMain extends ListenerAdapter 
{

    public static void main(String[] args) throws Exception 
    {
        // Remplace "YOUR_TOKEN" par le token de ton bot
        JDABuilder builder = JDABuilder.createDefault("MTE4NzQ4OTg0NDU0NTQ2MjMwMg.GmeD6P.Ocy-tQ-yGdSqA48cNqvn24Ar1aBluUo4Eh8mpQ");
        
        // Définit le statut du bot
        builder.setActivity(Activity.playing("Développer des bots"));

        // Ajouter un listener pour les messages
        builder.addEventListeners(new BotMain());

        // Se connecter
        builder.build();
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        // Si le bot reçoit "ping", il répond "pong"
        if (event.getMessage().getContentRaw().equals("!ping")) 
        {
            event.getChannel().sendMessage("pong!").queue();
        }
    }
}