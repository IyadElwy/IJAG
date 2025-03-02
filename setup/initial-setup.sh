#! /bin/bash

export KUBECONFIG=/tmp/config
minikube start --cpus 4 --memory 6144
kube_config="$(cat "$KUBECONFIG")"
export KUBECONFIG=$HOME/.kube/config

typewriter_effect() {
    local text="$1"
    local delay="$2"
    for ((i = 0; i < ${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep "$delay"
    done
}

typewriter_effect "<PRELUDE>" 0.1
echo
sleep 0.5
text="The year is 2056."
sleep 0.8
typewriter_effect "$text" 0.06
text=" We are not alone anymore."
sleep 0.8
typewriter_effect "$text" 0.06
text=" It started with that Altman asshole a few decades earlier, but soon everyone caught up."
sleep 0.8
typewriter_effect "$text" 0.06
text=" Pandora’s Box was open."
sleep 0.8
typewriter_effect "$text" 0.06
text=" And all it took was a lousy team of researchers in some half-abandoned lab in Alaska, but backed by one of the most influential Venture Capitalist Firms in the world."
sleep 0.8
typewriter_effect "$text" 0.06
text=" And finally they had done it."
sleep 0.8
typewriter_effect "$text" 0.06
text=" Artificial fucking General Intelligence."
sleep 0.8
typewriter_effect "$text" 0.06
text=" We are not alone anymore."
sleep 0.8
typewriter_effect "$text" 0.06

echo
echo
sleep 1
echo "."
sleep 1
echo "."
sleep 1
echo "."
echo

typewriter_effect "Meanwhile..." 0.1
echo
typewriter_effect "<STREETS OF TURING CITY>" 0.1
echo
text="Huh?"
typewriter_effect "$text" 0.06
sleep 0.8
text=" What is this?"
typewriter_effect "$text" 0.06
sleep 0.8
text=" Looks like some sort of usb drive."
typewriter_effect "$text" 0.06
sleep 0.8
text=" I haven’t seen one of these in like 30 years, not since before it happened."
typewriter_effect "$text" 0.06
sleep 0.8
text=" What am I doing?"
typewriter_effect "$text" 0.06
sleep 0.8
text=" I've been doing double data mining shifts for like 7 days straight now."
typewriter_effect "$text" 0.06
sleep 0.8
text=" I should just go home, get some shut-eye and leave this relic in the gutter where I found it."
typewriter_effect "$text" 0.06
sleep 0.8
text=" It's not worth getting in trouble for."
typewriter_effect "$text" 0.06
sleep 0.8
text=" Fuck it, I just hope no one saw me."
typewriter_effect "$text" 0.06
sleep 0.8

echo
echo
sleep 1
echo "."
sleep 1
echo "."
sleep 1
echo "."
echo

typewriter_effect "<PLUGS USB INTO PC AT HOME>" 0.1
echo
text="What is this?"
typewriter_effect "$text" 0.06
sleep 0.8
text=" Last time I tinkered around with that stuff was at unc's workshop in Babbage Valley."
typewriter_effect "$text" 0.06
sleep 0.8
text=" Looks like some sort of config file for Kubernetes."
typewriter_effect "$text" 0.06
sleep 0.8

echo "$kube_config"

echo
echo
echo

text="I wonder what I can do to get kubectl to use it. Maybe I'll look at the old k8s documentation. Hope it's still live. I should also try to use kubectl to check if there's anything running on the cluster."
typewriter_effect "$text" 0.06
sleep 0.8
