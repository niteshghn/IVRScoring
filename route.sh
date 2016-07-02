so_li_id=`pactl list short source-outputs | head -c3`
# echo `pactl list short source-outputs`
`pactl move-source-output $so_li_id 1`
# echo `pactl list short source-outputs`