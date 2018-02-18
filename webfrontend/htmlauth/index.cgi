#!/usr/bin/perl

# This is a sample Script file
# It does not much:
#   * Loading configuration
#   * including header.htmlfooter.html
#   * and showing a message to the user.
# That's all.

use File::HomeDir;
use CGI qw/:standard/;
use Config::Simple;
use Cwd 'abs_path';
use IO::Socket::INET;
use HTML::Entities;
use String::Escape qw( unquotemeta );
use warnings;
use strict;
no strict "refs"; # we need it for template system

my  $home = File::HomeDir->my_home;
our $lang;
my  $installfolder;
my  $cfg;
my  $conf;
our $psubfolder;
our $template_title;
our $namef;
our $value;
our %query;
our $phrase;
our $phraseplugin;
our $languagefile;
our $languagefileplugin;
our $cache;
our $savedata;
our $MSselectlist;
our $username;
our $password;
our $miniserver;
our $msudpport;
our $enabled;
our $localtime;
our $Enabledlist;
our $Localtimelist;

# ---------------------------------------
# Read Settings
# ---------------------------------------
$cfg             = new Config::Simple("$home/config/system/general.cfg");
$installfolder   = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");


print "Content-Type: text/html\n\n";

# ---------------------------------------
# Parse URL
# ---------------------------------------
foreach (split(/&/,$ENV{"QUERY_STRING"}))
{
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}

# ---------------------------------------
# Set parameters coming in - GET over POST
# ---------------------------------------
if ( !$query{'username'} )   { if ( param('username')  ) { $username = quotemeta(param('username'));         } 
else { $username = $username;  } } else { $username = quotemeta($query{'username'});   }

if ( !$query{'password'} )   { if ( param('password')  ) { $password = quotemeta(param('password'));         } 
else { $password = $password;  } } else { $password = quotemeta($query{'password'});   }

if ( !$query{'miniserver'} )   { if ( param('miniserver')  ) { $miniserver = quotemeta(param('miniserver'));         } 
else { $miniserver = $miniserver;  } } else { $miniserver = quotemeta($query{'miniserver'});   }

if ( !$query{'msudpport'} )   { if ( param('msudpport')  ) { $msudpport = quotemeta(param('msudpport'));         } 
else { $msudpport = $msudpport;  } } else { $msudpport = quotemeta($query{'msudpport'});   }	

if ( !$query{'enabled'} )   { if ( param('enabled')  ) { $enabled = quotemeta(param('enabled'));         } 
else { $enabled = $enabled;  } } else { $enabled = quotemeta($query{'enabled'});   }

if ( !$query{'localtime'} )   { if ( param('localtime')  ) { $localtime = quotemeta(param('localtime'));         } 
else { $localtime = $localtime;  } } else { $localtime = quotemeta($query{'localtime'});   }


# ---------------------------------------
# Figure out in which subfolder we are installed
# ---------------------------------------
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;


# ---------------------------------------
# Save settings to config file
# ---------------------------------------
if (param('savedata')) {
	$conf = new Config::Simple("$home/config/plugins/$psubfolder/netatmo.cfg");

	if ($enabled ne 1) { $enabled = 0 }

	if ($localtime ne 1) { $localtime = 0 }
	
	$username = encode_entities($username);
	print STDERR "$username\n";

	$conf->param('NETATMO.USERNAME', unquotemeta($username));
	$conf->param('NETATMO.PASSWORD', unquotemeta($password));
	$conf->param('NETATMO.MINISERVER', unquotemeta("MINISERVER$miniserver"));
	$conf->param('NETATMO.UDPPORT', unquotemeta($msudpport));
	$conf->param('NETATMO.ENABLED', unquotemeta($enabled));
	$conf->param('NETATMO.LOCALTIME', unquotemeta($localtime));
	
	$conf->save();
}


# ---------------------------------------
# Parse config file
# ---------------------------------------
$conf = new Config::Simple("$home/config/plugins/$psubfolder/netatmo.cfg");
$username = encode_entities($conf->param('NETATMO.USERNAME'));
$password = encode_entities($conf->param('NETATMO.PASSWORD'));
$miniserver = encode_entities($conf->param('NETATMO.MINISERVER'));
$msudpport = encode_entities($conf->param('NETATMO.UDPPORT'));
$enabled = encode_entities($conf->param('NETATMO.ENABLED'));
$localtime = encode_entities($conf->param('NETATMO.LOCALTIME'));


# ---------------------------------------
# Set Enabled / Disabled switch
# ---------------------------------------
if ($enabled eq "1") {
	$Enabledlist = '<option value="0">No</option><option value="1" selected>Yes</option>\n';
} else {
	$Enabledlist = '<option value="0" selected>No</option><option value="1">Yes</option>\n';
}

# ---------------------------------------
# Set Localtime Enabled / Disabled switch
# ---------------------------------------
if ($localtime eq "1") {
	$Localtimelist = '<option value="0">No</option><option value="1" selected>Yes</option>\n';
} else {
	$Localtimelist = '<option value="0" selected>No</option><option value="1">Yes</option>\n';
}


# ---------------------------------------
# Fill Miniserver selection dropdown
# ---------------------------------------
for (my $i = 1; $i <= $cfg->param('BASE.MINISERVERS');$i++) {
	if ("MINISERVER$i" eq $miniserver) {
		$MSselectlist .= '<option selected value="'.$i.'">'.$cfg->param("MINISERVER$i.NAME")."</option>\n";
	} else {
		$MSselectlist .= '<option value="'.$i.'">'.$cfg->param("MINISERVER$i.NAME")."</option>\n";
	}
}


# Init Language
	# Clean up lang variable
	$lang         =~ tr/a-z//cd; $lang         = substr($lang,0,2);
  # If there's no language phrases file for choosed language, use german as default
		if (!-e "$installfolder/templates/system/$lang/language.dat") 
		{
  		$lang = "de";
	}
	# Read translations / phrases
		$languagefile 			= "$installfolder/templates/system/$lang/language.dat";
		$phrase 						= new Config::Simple($languagefile);
		$languagefileplugin = "$installfolder/templates/plugins/$psubfolder/$lang/language.dat";
		$phraseplugin 			= new Config::Simple($languagefileplugin);



# Title
$template_title = $phrase->param("TXT0000") . ": Netatmo";

# ---------------------------------------
# Load header and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
# ---------------------------------------
open(F,"$installfolder/templates/system/$lang/header.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# ---------------------------------------
# Load content from template
# ---------------------------------------
open(F,"$installfolder/templates/plugins/$psubfolder/$lang/content.html") || die "Missing template $lang/content.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# ---------------------------------------
# Load footer and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
# ---------------------------------------
open(F,"$installfolder/templates/system/$lang/footer.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

exit;
