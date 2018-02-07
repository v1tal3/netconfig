jQuery(function($, undefined) {
    $('#term_demo').terminal(function(command) {
        console.log(command)
        if (command == 'help') {
          this.echo("Type the following.\n");
          this.echo("1. Companies worked for or experience=> exp");
          this.echo("2. Socials => social\n");
        }
        else if (command == 'social'){
          this.echo("mailto:gaurav.dev.iiitm@gmail.com\n");
          this.echo("https://www.github.com/chowmean\n");
          this.echo("https://www.facebook.com/chowmean\n");
          this.echo("https://www.twitter.com/gauravchowmean\n");
          this.echo("https://www.linkedin.com/in/chowmean\n");
        }
        else {
            if (command !== '') {
                try {
                    var result = window.eval(command);
                    if (result !== undefined) {
                        this.echo(new String(result));
                    }
                } catch(e) {
                    this.error(new String(e));
                }
            } else {
            this.echo('');
            }
        }
    }, {
        greetings: 'Javascript Interpreter',
        name: 'js_demo',
        height: 200,
        prompt: 'js> '
    });
});