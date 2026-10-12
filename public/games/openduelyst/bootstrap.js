const {Scene,PackageManager,packages}=window.duelystRendererProbe;
const {GameSession,Sandbox,FactionFactory,DrawStartingHandAction:Draw}=window.duelystLocalSDKProbe;
const saveKey='duelyst-local-player-save-v1';
const status=document.getElementById('status');
(async()=>{
 await Scene.setup();GameSession.reset();const game=GameSession.current();
 const saved=localStorage.getItem(saveKey);
 if(saved){const data=JSON.parse(saved);game.deserializeSessionFromFirebase(JSON.parse(data.snapshot));game.setUserId(data.userId);if(!game.isSandbox())throw Error('Local save must be Sandbox');game.setIsRunningAsAuthoritative(true);}
 else{game.setUserId('local-player');const challenge=new Sandbox();challenge.setPlayer1DeckData(FactionFactory.starterDeckForFactionLevel(1));challenge.setPlayer2DeckData(FactionFactory.starterDeckForFactionLevel(2));challenge.setupSession(game);for(const p of game.getPlayers())game.executeAction(new Draw(game,p.getPlayerId(),[]));}
 for(const name of ['game','faction_game_1','faction_game_2'])await PackageManager.current().loadPackage(name,packages[name]);
 await Scene.current().showGame();const layer=Scene.current().getGameLayer();layer.bottomDeckLayer.showStartingHand();await layer.showActiveGame();window.duelystRendererProbe.connectPointer();
 layer.getEventBus().on('after_show_end_turn',()=>{const g=GameSession.current();g.setUserId(g.getCurrentPlayer().getPlayerId());});
 document.getElementById('end-turn').onclick=()=>{const g=GameSession.current();if(layer.getIsMyTurn()&&!layer.getPlayerSelectionLocked()&&!g.isOver())g.submitExplicitAction(g.actionEndTurn());};
 document.getElementById('save').onclick=()=>{const g=GameSession.current();localStorage.setItem(saveKey,JSON.stringify({snapshot:g.generateGameSessionSnapshot(),userId:g.getUserId()}));status.textContent='Saved locally • audio off';};
 document.getElementById('concede').onclick=()=>{const g=GameSession.current();if(!g.isOver())g.submitExplicitAction(g.getMyPlayer().actionResign());};
 for(const b of document.querySelectorAll('button'))b.disabled=false;
 status.textContent='Local two-player Sandbox • audio off';window.localPlayerReady=true;
})().catch(e=>{status.textContent='Could not start local game';console.error(e);});
document.getElementById('new-game').onclick=()=>{localStorage.removeItem(saveKey);location.reload();};
