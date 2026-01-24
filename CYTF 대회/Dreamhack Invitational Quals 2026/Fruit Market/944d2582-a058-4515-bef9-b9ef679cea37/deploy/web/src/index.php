<?php
declare(strict_types=1);
ini_set('display_errors','1'); error_reporting(E_ALL);

$API_BASE = getenv('API_BASE_URL') ?: 'http://api:5000';
$API_BASE_NORM = rtrim($API_BASE, '/');
const REQUIRED_KEYS = ['album','artist','cover_url','duration_seconds','id','title','year'];



function safe_get(string $url): array 
{
    $raw = @file_get_contents($url);  # url에서 콘텐츠를 읽어와서 raw에 넣음
    $needles = ["DH{", "<"];
    if (array_filter($needles, fn($needle) => str_contains($raw, $needle)))   # url에서 읽어온 데이터 raw 중에서 needle(금지 문자열)이 있으면 아래 실행
    {
      return [null, 'Suspicious output!'];
    }
    # raw에 금지 문자열이 없다면 아래 실행

    # raw를 읽어들이는데 실패했다면 실패했다고 반환
    if ($raw === false) { $err = error_get_last(); return [null, 'Fetch failed']; }
    return [$raw, null];  # raw를 읽어들이는데 성공했다면 raw를 반환함
}






function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES); }
function missing_keys(array $obj, array $required): array {
    return array_values(array_diff($required, array_keys($obj)));
}



function sanitize_song_url(?string $u): ?string {
    if (!$u) return null;
    $u = trim($u);
    if (!filter_var($u, FILTER_VALIDATE_URL)) return null;
    if (!preg_match('/https?:\/\//i', $u)) return null;
    return $u;
}




$listError = null;  # listError는 처음에는 null
$songs = [];        # songs는 처음에는 빈 배열

[$rawList, $errList] = safe_get($API_BASE_NORM . '/songs');   # /songs를 가져옴
if ($errList) $listError = $errList;    # 데이터를 불러오는데 실패했다면 해당 에러를 listError에 할당함
else {    
    $decoded = json_decode($rawList, true); # JSON 데이터인 rawList를 PHP에서 다룰 수 있는 형태인 연관 배열로 바꿔서 decoded에 할당
    if (json_last_error() !== JSON_ERROR_NONE || !is_array($decoded)) $listError = 'Invalid data.';     # 위에서 수행한 json_decoded에서 에러가 발생했거나 decoded가 배열이 아니라면 listError에 "에러에용!" 이라고 하기
    else $songs = $decoded;   # decoded를 잘 불러오고 에러도 없고, 배열이기까지 하다면 songs에 할당하기
}





$detailError = null;  
$selected = null;     
$activeUrl = isset($_POST['song_url']) ? sanitize_song_url($_POST['song_url'] ?? null) : null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') 
{
    $url = sanitize_song_url($_POST['song_url'] ?? null);
    if (!$url) 
    {
        $detailError = 'Invalid data.';
    } 
    else 
      {
        [$rawOne, $errOne] = safe_get($url);
        if ($errOne) 
        {
            $detailError = $errOne;
        } 
        else 
        {
            $one = json_decode($rawOne, true);
            if (json_last_error() !== JSON_ERROR_NONE || !is_array($one)) 
            {
                $detailError = 'Invalid data.';
            } 
            else 
            {
                $missing = missing_keys($one, REQUIRED_KEYS);
                if ($missing) $detailError = 'Invalid data.';
                else $selected = $one;
            }
        }
    }
}



function render_song_row(array $s, bool $isActive, string $api_base_norm): string {
    $id     = h((string)($s['id'] ?? ''));
    $title  = h((string)($s['title'] ?? 'Untitled'));
    $artist = h((string)($s['artist'] ?? ''));
    $album  = h((string)($s['album'] ?? ''));
    $year   = h((string)($s['year'] ?? ''));
    $rowUrl = h($api_base_norm . '/songs/' . rawurlencode((string)($s['id'] ?? '')));
    $cls    = $isActive ? 'song-row active' : 'song-row';
    return <<<HTML
    <form method="POST" class="$cls">
      <button type="submit" name="song_url" value="$rowUrl" class="row-btn" title="Open $title">
        <div class="row-main">
          <div class="row-title">$title</div>
          <div class="row-sub">$artist • $album • $year</div>
        </div>
        <div class="row-chevron" aria-hidden="true">›</div>
      </button>
    </form>
    HTML;
}

function render_detail(?array $s): string {
    if(!$s) return '<div class="card"><em>Select a song from the left panel to view details.</em></div>';
    $title  = h((string)($s['title'] ?? 'Untitled'));
    $artist = h((string)($s['artist'] ?? ''));
    $album  = h((string)($s['album'] ?? ''));
    $year   = h((string)($s['year'] ?? ''));
    $dur    = isset($s['duration_seconds']) ? h((string)$s['duration_seconds'].'s') : '';
    $cover  = !empty($s['cover_url'])
        ? '<img class="cover-lg" src="'.h((string)$s['cover_url']).'" alt="Album art" />'
        : '<div class="cover-lg placeholder" aria-hidden="true"></div>';
    return <<<HTML
    <div class="card detail-card">
      <div class="detail-inner">
        $cover
        <div class="meta-stack">
          <div class="meta-line title">$title</div>
          <div class="meta-line"><span class="label">Artist</span><span class="value">$artist</span></div>
          <div class="meta-line"><span class="label">Album</span><span class="value">$album</span></div>
          <div class="meta-line"><span class="label">Year</span><span class="value">$year</span></div>
          <div class="meta-line"><span class="label">Duration</span><span class="value">$dur</span></div>
        </div>
      </div>
    </div>
    HTML;
}
?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Jukebox</title>
<style>
:root{
  --bg:#0b0b12; --panel:#101022; --card:#141426; --accent:#ff4fd8; --accent-2:#3df5ff;
  --text:#e8e8f2; --muted:#a0a3b1; --border:#2a2a4a;
  --pane-h:72vh; --right-w:720px;
}
*{box-sizing:border-box}
body{margin:0;padding:0;background:radial-gradient(1200px 600px at 10% 0%,#16162e 0%,var(--bg) 50%),
  radial-gradient(800px 400px at 90% 10%,#0e1c2b 0%,transparent 60%);color:var(--text);
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Inter,"Noto Sans",Arial,sans-serif;min-height:100vh;display:grid;place-items:center}
.wrap{width:min(100%,1200px);padding:24px}
.hero{display:grid;gap:10px;justify-items:center;text-align:center;margin-bottom:16px}
.disc{width:90px;height:90px;border-radius:50%;background:
  radial-gradient(circle at 50% 50%,#000 0 8px,#29293f 10px 44px,#111 46px 100%),
  repeating-radial-gradient(circle at 50% 50%,rgba(255,255,255,.06) 0 2px,rgba(255,255,255,0) 2px 4px);
  box-shadow:0 0 0 6px rgba(255,255,255,.06),0 30px 60px rgba(0,0,0,.55);animation:spin 8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
h1{font-size:clamp(22px,3vw,34px);background:linear-gradient(90deg,var(--accent),var(--accent-2));
  -webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 0 12px rgba(61,245,255,.25);margin:8px 0 0 0}
p.sub{color:var(--muted);margin:0}

.app{display:grid;grid-template-columns:minmax(300px,1fr) var(--right-w);gap:18px;align-items:start}
.panel,.right{height:var(--pane-h)}
.panel{
  background:linear-gradient(180deg,#171733 0%,#0d0d1b 100%);border:1px solid var(--border);border-radius:18px;padding:12px;
  box-shadow:0 20px 60px rgba(0,0,0,.35);overflow-y:auto;overflow-x:hidden;min-width:260px
}
.panel h3{margin:6px 8px 10px;font-size:16px;color:var(--muted)}
.song-row{margin:0;padding:0;background:transparent;border:0;display:block}
.row-btn{
  width:100%;display:grid;grid-template-columns:1fr auto;align-items:center;gap:10px;text-align:left;padding:10px 12px;cursor:pointer;
  color:var(--text);background:#0b0b19;border:1px solid var(--border);border-radius:12px;transition:background .15s,transform .05s,border-color .15s
}
.row-btn:hover{background:#0f0f20;border-color:var(--accent);box-shadow:0 0 0 6px rgba(255,79,216,.15)}
.song-row + .song-row{margin-top:10px}
.row-main{overflow:hidden}
.row-title{font-weight:700;white-space:nowrap;text-overflow:ellipsis;overflow:hidden}
.row-sub{color:var(--muted);font-size:12px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden}
.row-chevron{font-size:24px;color:var(--muted)}
.song-row.active .row-btn{border-color:var(--accent);box-shadow:0 0 0 6px rgba(255,79,216,.15)}

.right{
  border:1px solid var(--border);border-radius:18px;background:transparent;padding:0;
  overflow-y:auto;overflow-x:hidden;min-width:0;width:100%;
}
.right-inner{display:grid;gap:18px;padding:12px;width:100%;max-width:100%}

.card{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:16px;box-shadow:0 12px 30px rgba(0,0,0,.35);
  width:100%;max-width:100%}

.detail-card{display:grid;place-items:center;text-align:center}
.detail-inner{width:100%;max-width:100%;display:grid;gap:14px;justify-items:center}
.cover-lg{
  width:min(90%, 360px); aspect-ratio:1/1; display:block; margin:0 auto;
  border-radius:16px; object-fit:cover; background:#0b0b19; border:1px solid var(--border);
}
.cover-lg.placeholder{background:linear-gradient(135deg,#0b0b19,#101028)}
.meta-stack{width:min(95%, 560px); max-width:100%; display:grid; gap:8px; text-align:left}
.meta-line{display:grid;grid-template-columns:120px minmax(0,1fr);gap:8px;align-items:center}
.meta-line.title{grid-template-columns:1fr; font-weight:800; font-size:22px; text-align:center; overflow-wrap:anywhere; margin-bottom:6px}
.label{color:var(--muted)}
.value{color:var(--text); overflow-wrap:anywhere}

@media (max-width:900px){
  .app{grid-template-columns:1fr}
  .panel,.right{height:auto}
  .meta-line{grid-template-columns:100px minmax(0,1fr)}
}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <div class="disc" aria-hidden="true"></div>
    <h1>Jukebox</h1>
  </div>

  <div class="app">
    <div class="panel">
      <h3>All Songs</h3>
      <?php if ($listError): ?>
        <div class="card"><strong>List error:</strong> <?= h($listError) ?></div>
      <?php elseif (!$songs): ?>
        <div class="card"><em>No songs found.</em></div>
      <?php else: ?>
        <?php
          foreach ($songs as $s) {
            $rowUrl = $API_BASE_NORM . '/songs/' . rawurlencode((string)($s['id'] ?? ''));
            $isActive = ($activeUrl && $activeUrl === $rowUrl);
            echo render_song_row($s, (bool)$isActive, $API_BASE_NORM);
          }
        ?>
      <?php endif; ?>
    </div>

    <div class="right">
      <div class="right-inner">
        <?php if ($detailError): ?>
          <div class="card"><strong>Error:</strong> <?= h($detailError) ?></div>
        <?php else: ?>
          <?= render_detail($selected) ?>
        <?php endif; ?>
      </div>
    </div>
  </div>
</div>
</body>
</html>
