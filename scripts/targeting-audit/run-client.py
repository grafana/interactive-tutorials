#!/usr/bin/env python3
import io,os,pathlib,subprocess,sys,tarfile,tempfile
root=pathlib.Path(__file__).resolve().parents[2]
checkout=pathlib.Path(sys.argv[1]).resolve()
revision='37a9e12aa19ac269812242ddfba8b0d54ffa0a30'
with tempfile.TemporaryDirectory(prefix='tutorial-targeting-client-') as temp:
 p=pathlib.Path(temp)
 archive=subprocess.check_output(['git','archive',revision],cwd=checkout)
 with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(p,filter='data')
 (p/'node_modules').symlink_to((checkout/'node_modules').resolve())
 (p/'src/lib/tutorial-catalog-audit.test.ts').write_bytes((root/'scripts/targeting-audit/client.test.ts').read_bytes())
 env=dict(os.environ,AUDIT_RESULTS=str(root/'docs/targeting-audit/results.json'),AUDIT_SCENARIOS=str(root/'docs/targeting-audit/scenarios.json'),AUDIT_INVENTORY=str(root/'docs/targeting-audit/inventory.json'))
 subprocess.run(['npm','run','test:ci','--','--watch=false','--runTestsByPath','src/lib/tutorial-catalog-audit.test.ts','src/lib/recommendation-ranking.test.ts','src/lib/context-event-bus.test.ts'],cwd=p,env=env,check=True)
