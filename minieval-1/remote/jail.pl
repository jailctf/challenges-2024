#!/usr/local/bin/perl
select(STDOUT); $| = 1;

{
    print("> ");
    my $input = <STDIN>;
    chomp($input);
    if (length($input) > 5 or $input =~ /[\pL'"<>\\]/) {
        print("Bye!");
        exit(1)
    }

    $_ = eval($input);
    redo
}
